<template>
  <q-page class="flex items-center justify-center">
    <div class="relative w-full max-w-md mx-auto">
      <div
        class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"
      ></div>
      <div class="relative p-6 bg-white shadow-lg sm:rounded-3xl">
        <h1 class="text-3xl mb-4">Virtual Teacher</h1>
        <div v-if="!isStarted" class="mb-4">
          <q-btn color="primary" label="Start" @click="start" />
        </div>
        <div v-else class="">
          <!-- v-align to bottom -->
          <div
            id="messages"
            class="my-5 overflow-auto flex flex-col-reverse"
          >
            <div v-for="(message, index) in messages" :key="index" class="mb-2">
              <strong>{{ message.sender }}:</strong> {{ message.text }}
            </div>
            <div v-if="isLoading" class="flex justify-center">
              <q-spinner-dots color="primary" size="2em" />
            </div>
          </div>

          <message-component
            :is-recording="isRecording"
            :startRecording="startRecording"
            :stopRecording="stopRecording"
            @send-message="onSendMessage"
          />

          <audio id="responseAudio" class="hidden" controls></audio>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import MessageComponent from "pages/MessageComponent.vue";

const host = "https://a124-2a0b-6204-41fa-e200-e1a6-a202-373f-2f2c.ngrok.io";
export default {
  components: { MessageComponent },
  data() {
    return {
      recorder: null,
      audioContext: null,
      messages: [],
      isRecording: false,
      isLoading: false,
      isStarted: false,
    };
  },
  methods: {
    async start() {
      this.isLoading = true;
      this.isStarted = true;
      const response = await fetch(host + "/start");
      const data = await response.json();
      this.processAnswer(data.text);
      this.isLoading = false;
    },
    onSendMessage(message) {
      if (message.trim()) {
        this.process_user_message({ text: message });
        // handle sending the message to the AI
      }
    },

    async startRecording() {
      console.log("start recording");
      this.isRecording = true;
      this.audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.recorder = new MediaRecorder(stream);
      this.recorder.start();
    },

    process_user_message: async function (data) {
      this.displayMessage("User", data.text);

      const responseMessage = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: data.text }),
      });
      const resp = await responseMessage.json();
      const answer = resp.answer;
      this.processAnswer(answer);
      this.isLoading = false;
    },

    async stopRecording() {
      this.isLoading = true;
      this.isRecording = false;
      this.recorder.stop();
      this.recorder.addEventListener("dataavailable", async (e) => {
        const audioBlob = e.data;
        const formData = new FormData();
        formData.append("audio", audioBlob);
        const response = await fetch("http://localhost:8000/speach-to-text", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        await this.process_user_message(data);
      });
    },

    displayMessage(sender, message) {
      // this.messages.push({ sender, text: message });
      // add to the end of the array
      this.messages.unshift({ sender, text: message });
    },

    processAnswer(answer) {
      const ttsUrl = `http://localhost:8000/text-to-speech?text=${encodeURIComponent(
        answer
      )}`;
      const responseAudio = document.getElementById("responseAudio");
      responseAudio.src = ttsUrl;
      responseAudio.play();
      this.displayMessage("AI", answer);
    },
  },
};
</script>
