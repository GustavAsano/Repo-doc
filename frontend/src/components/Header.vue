<template>
  <v-app-bar :elevation="1" class="bg-white pl-8 pr-4">
    <template #prepend>
      <div class="h-100 pr-4 pl-4">
        <a href="https://genms-playground.com/" target="_blank" class="gen-ms-logo"
          ><img src="/LogoGenMS.png" style="image-rendering: crisp-edges"
        /></a>
      </div>
      <v-divider class="mx-2" inset vertical></v-divider>
    </template>
    <v-app-bar-title class="text-primary font-weight-black">
      <span class="text-h4">Repository Documentation <v-icon size="x-small" icon="mdi-clipboard-text" /></span>
    </v-app-bar-title>
    <v-spacer></v-spacer>

    <v-dialog v-model="infoDialog" max-width="70%">
      <template #activator="{ props: activatorProps }">
        <v-btn prepend-icon="mdi-information-outline" v-bind="activatorProps" color="surface-variant">Info</v-btn>
      </template>

      <template #default>
        <v-card title="GenMS - Repository Documentation">
          <v-card-text>
            Repository Documentation is an AI project developed by the GenMS team in
            <a href="https://www.managementsolutions.com" target="_blank">Management Solutions</a>.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="infoDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
  </v-app-bar>
</template>

<script setup>
import { ref } from 'vue';

const infoDialog = ref(false);
</script>

<style scoped>
.gen-ms-logo {
  width: auto;
  max-width: auto;
  height: 100%;
  display: flex;
  align-items: center;
}

.gen-ms-logo img {
  height: auto;
  height: 60%;
}
</style>
