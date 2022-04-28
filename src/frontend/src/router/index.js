import Vue from "vue";
import VueRouter from "vue-router";
import Search from "../views/Search.vue";
// import SearchAdvanced from "../views/SearchAdvanced.vue";
import DocumentResults from "../views/DocumentResults.vue";
// import AuthorResults from "../views/AuthorResults.vue";
// import VenueResults from "../views/VenueResults.vue";
// import VideoResults from "../views/VideoResults.vue";
import DocumentDetails from "../views/DocumentDetails.vue";
// import Appendix from "../views/Appendix.vue";
// import Timeline from "../views/Timeline.vue";
// import VisitMap from "../views/VisitMap.vue";
// import Dashboard from "../views/Dashboard.vue";
// import Maintain from "../views/Maintain.vue";
import Mistake from "../views/Mistake.vue";

Vue.use(VueRouter);

const routerPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(error => error);
};

const routes = [
  {
    path: "/",
    name: "Search",
    component: Search,
    meta: {
      title: "Home",
      keepAlive: true
    }
  },
  // {
  //   path: "/adv",
  //   name: "SearchAdvanced",
  //   component: SearchAdvanced,
  //   meta: {
  //     title: "Home",
  //     keepAlive: true
  //   }
  // },
  {
    path: "/docs",
    name: "DocumentResults",
    component: DocumentResults,
    meta: {
      title: "Results",
      keepAlive: false
    }
  },
  // {
  //   path: "/auth",
  //   name: "AuthorResults",
  //   component: AuthorResults,
  //   meta: {
  //     title: "Results",
  //     keepAlive: false
  //   }
  // },
  // {
  //   path: "/affi",
  //   name: "VenueResults",
  //   component: VenueResults,
  //   meta: {
  //     title: "Results",
  //     keepAlive: false
  //   }
  // },
  // {
  //   path: "/film",
  //   name: "VideoResults",
  //   component: VideoResults,
  //   meta: {
  //     title: "Results",
  //     keepAlive: false
  //   }
  // },
  {
    path: "/full",
    name: "DocumentDetails",
    component: DocumentDetails,
    meta: {
      title: "DocDetails",
      keepAlive: false
    }
  },
  // {
  //   path: "/note",
  //   name: "Appendix",
  //   component: Appendix,
  //   meta: {
  //     title: "Appendix",
  //     keepAlive: false
  //   }
  // },
  // {
  //   path: "/time",
  //   name: "Timeline",
  //   component: Timeline,
  //   meta: {
  //     title: "Timeline",
  //     keepAlive: false
  //   }
  // },
  // {
  //   path: "/map",
  //   name: "VisitMap",
  //   component: VisitMap,
  //   meta: {
  //     title: "VisitMap",
  //     keepAlive: false
  //   }
  // },
  // {
  //   path: "/board",
  //   name: "Dashboard",
  //   component: Dashboard,
  //   meta: {
  //     title: "Dashboard",
  //     keepAlive: false
  //   }
  // },
  // {
  //   path: "/sorry",
  //   name: "Maintain",
  //   component: Maintain,
  //   meta: {
  //     title: "Maintain",
  //     keepAlive: false
  //   }
  // },
  {
    path: "/*",
    name: "Mistake",
    component: Mistake,
    meta: {
      title: "Home",
      keepAlive: false
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
