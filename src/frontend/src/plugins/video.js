import Vue from "vue";
import VueYouTubeEmbed from "vue-youtube-embed";
import VueVimeoPlayer from "vue-vimeo-player";

Vue.use(VueYouTubeEmbed, { global: true, componentId: "youtube-player" });
Vue.use(VueVimeoPlayer);
