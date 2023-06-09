<template>
  <q-page class="flex items-center justify-center font-roboto">
    <div class="relative w-full max-w-md mx-auto h-full">
      <div
        class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-xl transition-all duration-500 ease-in-out"
      ></div>
      <div class="relative p-6 bg-white shadow-lg sm:rounded-xl">
        <h1 class="text-3xl mb-2">Speak Fluent</h1>
        <h2 class="text-xl mb-6 text-gray-600 italic">Your AI English Tutor, Anytime, Anywhere</h2>
        <div v-if="!isStarted" class="mb-4">
          <q-btn color="primary" label="Start" @click="start" class="shadow-md hover:shadow-lg"/>
        </div>
        <div v-else class="">
          <div
            id="messages"
            class="my-5 overflow-auto flex flex-col-reverse"
          >
            <div v-if="isLoading" class="flex justify-center">
              <q-spinner-dots color="primary" size="2em"/>
            </div>
            <div v-for="(message, index) in messages" :key="index" class="mb-3">
              <strong>{{ message.sender }}:</strong> {{ message.text }}
            </div>
          </div>

          <message-component
            :is-recording="isRecording"
            :startRecording="startRecording"
            :stopRecording="stopRecording"
            @send-message="onSendMessage"
            class="hover:bg-blue-100 transition-colors duration-300 ease-in-out"
          />

          <audio id="responseAudio" class="hidden" controls></audio>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.font-roboto {
  font-family: 'Roboto', sans-serif;
}
</style>



<script>
import MessageComponent from "pages/MessageComponent.vue";

const host = "http://localhost:8000";
export default {
  components: {MessageComponent},
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
      const response = await fetch(`${process.env.HOST}/start`);
      const data = await response.json();
      this.processAnswer(data.text);
    },
    onSendMessage(message) {
      if (message.trim()) {
        this.process_user_message({text: message});
        // handle sending the message to the AI
      }
    },

    async startRecording() {
      console.log("start recording");
      this.isRecording = true;
      this.audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      const stream = await navigator.mediaDevices.getUserMedia({audio: true});
      this.recorder = new MediaRecorder(stream);
      this.recorder.start();
    },

    process_user_message: async function (data) {
      this.displayMessage("User", data.text);

      const responseMessage = await fetch(`${process.env.HOST}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({text: data.text}),
      });
      const resp = await responseMessage.json();
      const answer = resp.answer;
      this.processAnswer(answer);

    },

    async stopRecording() {
      this.isLoading = true;
      this.isRecording = false;
      this.recorder.stop();
      this.recorder.stream.getTracks().forEach(track => track.stop());

      this.recorder.addEventListener("dataavailable", async (e) => {
        const audioBlob = e.data;
        const formData = new FormData();
        formData.append("audio", audioBlob);
        const response = await fetch(`${process.env.HOST}/speach-to-text`, {
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
      this.messages.unshift({sender, text: message});
    },

    processAnswer(answer) {
      const ttsUrl = `${process.env.HOST}/text-to-speech?text=${encodeURIComponent(
        answer
      )}`;
      const responseAudio = document.getElementById("responseAudio");
      responseAudio.src = ttsUrl;
      responseAudio.play()
        .then(() => {
          this.displayMessage("AI", answer);
        })
        .catch((error) => {
          console.error("Error playing audio:", error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    }

  },
}
;
</script>
