<template>
  <div class="flex w-full">
    <q-input
      :disabled="isRecording"
      v-model="messageText"
      label="Type your message"
      class="mr-2 flex-grow"
      @keyup.enter="sendMessage"
      @keyup.esc="messageText = ''"
    />
    <q-btn
      :disabled="isRecording"
      color="primary"
      dense
      @click="sendMessage"
      class="mr-1"
    >
      <q-icon name="send" />
    </q-btn>
    <!-- onclick do startRecording if not recording, else do stopRecording -->
    <q-btn
      :class="{
        'bg-blue-700': isRecording,
        'shadow-inner': isRecording,
      }"
      color="primary"
      class="flex items-center justify-center primary"
      @click="isRecording ? stopRecording() : startRecording()"
    >
      <q-icon
        v-if="!isRecording"
        class="text-white"
        name="keyboard_voice"
      />
      <q-icon v-else class="text-white" name="stop" />
    </q-btn>
  </div>
</template>

<script>
export default {
  name: "MessageComponent",
  props: {
    isRecording: {},
    startRecording: {},
    stopRecording: {},
  },
  data() {
    return {
      messageText: "",
    };
  },
  methods: {
    sendMessage() {
      this.$emit("send-message", this.messageText);
      this.messageText = "";
    },
  },
};
</script>
