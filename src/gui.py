import queue
import threading

import dearpygui.dearpygui as dpg

from src.ollama_client import OllamaClient


class OllamaChatApp:
    """
    Desktop chat GUI application using DearPyGui and the local Ollama API.
    This avoids macOS Tk rendering issues while keeping a real desktop GUI.
    """

    def __init__(self):
        self.client = OllamaClient()
        self.messages = []
        self.chat_log = "System:\nLocal Ollama chat is ready. Type a message below and press Send.\n\n"
        self.response_queue = queue.Queue()
        self.waiting_for_response = False

        dpg.create_context()
        self._build_ui()

    def _build_ui(self):
        dpg.create_viewport(title="Local Ollama Chat", width=780, height=640)

        with dpg.window(label="Local Ollama Chat", tag="main_window", width=780, height=640):
            dpg.add_text("Local Ollama Chat", color=(30, 30, 30))
            dpg.add_text(f"Model: {self.client.model} | API: local Ollama")
            dpg.add_separator()

            dpg.add_input_text(
                tag="chat_display",
                default_value=self.chat_log,
                multiline=True,
                readonly=True,
                width=-1,
                height=430
            )

            dpg.add_separator()

            dpg.add_input_text(
                tag="user_input",
                hint="Type your message here...",
                width=520,
                on_enter=True,
                callback=self.send_message
            )

            dpg.add_same_line()
            dpg.add_button(
                label="Send",
                tag="send_button",
                width=90,
                callback=self.send_message
            )

            dpg.add_same_line()
            dpg.add_button(
                label="Clear Chat",
                tag="clear_button",
                width=110,
                callback=self.clear_chat
            )

            dpg.add_text("Status: Ready", tag="status_label")

        dpg.setup_dearpygui()
        dpg.set_primary_window("main_window", True)

    def mainloop(self):
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            self._process_response_queue()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def _append_to_chat(self, sender, text):
        self.chat_log += f"{sender}:\n{text}\n\n"
        dpg.set_value("chat_display", self.chat_log)

    def send_message(self, sender=None, app_data=None, user_data=None):
        if self.waiting_for_response:
            return

        user_text = dpg.get_value("user_input").strip()

        if not user_text:
            dpg.set_value("status_label", "Status: Cannot send an empty message.")
            return

        self._append_to_chat("You", user_text)
        self.messages.append({"role": "user", "content": user_text})
        dpg.set_value("user_input", "")

        self._set_controls_enabled(False)
        dpg.set_value("status_label", "Status: Thinking...")
        self.waiting_for_response = True

        worker = threading.Thread(target=self._fetch_response, daemon=True)
        worker.start()

    def _fetch_response(self):
        try:
            response = self.client.chat(self.messages)
            self.response_queue.put(("success", response))
        except Exception as exc:
            self.response_queue.put(("error", str(exc)))

    def _process_response_queue(self):
        while not self.response_queue.empty():
            result_type, payload = self.response_queue.get()

            if result_type == "success":
                self.messages.append({"role": "assistant", "content": payload})
                self._append_to_chat("Ollama", payload)
                dpg.set_value("status_label", "Status: Ready")
            else:
                self._append_to_chat("System Error", payload)
                dpg.set_value("status_label", "Status: Connection/API Error")

            self.waiting_for_response = False
            self._set_controls_enabled(True)

    def clear_chat(self):
        if self.waiting_for_response:
            return

        self.messages = []
        self.chat_log = "System:\nChat history cleared.\n\n"
        dpg.set_value("chat_display", self.chat_log)
        dpg.set_value("status_label", "Status: Chat history cleared")

    def _set_controls_enabled(self, enabled):
        dpg.configure_item("user_input", enabled=enabled)
        dpg.configure_item("send_button", enabled=enabled)
        dpg.configure_item("clear_button", enabled=enabled)
