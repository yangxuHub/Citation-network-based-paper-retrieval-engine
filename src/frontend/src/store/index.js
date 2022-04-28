import Vue from "vue";
import Vuex from "vuex";
import VueCookies from "vue-cookies";
import router from "@/router";
import { i18n } from "@/plugins/i18n.js";
import { Message } from "element-ui";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    //graph
    dataList: [],
    linkList: [],
    docList: [],
    // Input
    searchInput: "",
    // List
    currentPage: 1,
    // Range
    yearFrom: "",
    yearTo: "",
    // Field
    selectField: "title",
    fieldOptions: [
      {
        value: "title",
        label: i18n.t("home.fTITLE")
      },
      {
        value: "authors",
        label: i18n.t("home.fAUTHORS")
      },
      {
        value: "venue",
        label: i18n.t("home.fVENUE")
      },
      {
        value: "abstract",
        label: i18n.t("home.fABSTRACT")
      }
    ],
    // Logic
    selectLogic: "and",
    logicOptions: [
      {
        value: "and",
        label: i18n.t("home.lAND")
      },
      {
        value: "or",
        label: i18n.t("home.lOR")
      },
      {
        value: "not",
        label: i18n.t("home.lNOT")
      }
    ],
    // ListDocs
    listDocs: [],
    // Film
    selectFilm: "title",
    filmOptions: [
      {
        value: "title",
        label: i18n.t("film.fTITLE")
      },
      {
        value: "caption",
        label: i18n.t("film.fCAPTION")
      }
    ],
    // QA
    qaTalk: [],
    // Show
    fChatShow: false,
    fDrawerShow: false,
    // Maintain
    fHomeMaintain: false,
    fDocMaintain: false,
    fVideoMaintain: false,
    // IP
    ipLocal: ""
  },
  mutations: {
    //graph
    updateGraphData(state, data) {
      // console.log("更新dataGraph")
      state.dataList = data.dataList;
      state.linkList = data.linkList;
      state.docList = data.docList;
    },
    // Input
    updateInput(state, input) {
      state.searchInput = input;
    },
    // List
    updatePage(state, input) {
      state.currentPage = input;
    },
    // Range
    updateYearFrom(state, input) {
      state.yearFrom = input;
    },
    updateYearTo(state, input) {
      state.yearTo = input;
    },
    // Field
    updateField(state, input) {
      state.selectField = input;
    },
    updateFieldOptions(state) {
      state.fieldOptions.forEach(function(field) {
        field.label = i18n.t("home.f" + field.value.toUpperCase());
      }, this);
    },
    // Logic
    updateLogic(state, input) {
      state.selectLogic = input;
    },
    updateLogicOptions(state) {
      state.logicOptions.forEach(function(logic) {
        logic.label = i18n.t("home.l" + logic.value.toUpperCase());
      }, this);
    },
    // ListDocs
    resetListDocs(state) {
      state.listDocs = [];
    },
    increaseListDocs(state) {
      state.listDocs.push({
        logicOptions: state.logicOptions,
        logicInput: state.selectLogic,
        fieldOptions: state.fieldOptions,
        fieldInput:
          state.listDocs.length > 0
            ? state.listDocs[state.listDocs.length - 1].fieldInput
            : state.selectField,
        inputDoc: ""
      });
    },
    decreaseListDocs(state, index = 0) {
      state.listDocs.splice(index, 1);
    },
    updateListDocs(state) {
      state.listDocs.forEach(function(doc) {
        doc.logicOptions = state.logicOptions;
        doc.fieldOptions = state.fieldOptions;
      }, this);
    },
    // Film
    updateFilm(state, input) {
      state.selectFilm = input;
    },
    updateFilmOptions(state) {
      state.filmOptions.forEach(function(film) {
        film.label = i18n.t("film.f" + film.value.toUpperCase());
      }, this);
    },
    // QA
    pushQATalk(state, input) {
      state.qaTalk.push(input);
    },
    updateQATalk(state, input) {
      state.qaTalk[state.qaTalk.length - 1].plain = input;
    },
    // Show
    updateChatShow(state, input) {
      state.fChatShow = input;
    },
    updateDrawerShow(state, input) {
      state.fDrawerShow = input;
    },
    // IP
    updateIPLocal(state, input) {
      state.ipLocal = input;
    },
    // Query
    handleQuery(state, obj = {}) {
      var input = state.searchInput.toLowerCase();
      input = input.replace(/(^\s*)|(\s*$)/g, "");
      input = input.replace(/\s+/g, " ");
      state.searchInput = input;
      if (!input) {
        Message.error(i18n.t("home.CannotEmpty"));
        return;
      }
      if (!obj.adv) {
        obj.adv = !!input.match(/^\$(\w|\s|\(|\))+\$$/g);
        if (obj.adv) {
          Message.info(i18n.t("home.Change2Adv"));
        }
      }
      // Push
      if (!obj.film) {
        router.push({
          path: "/docs",
          query: { query: input, adv: !!obj.adv }
        });
      } else {
        router.push({
          path: "/film",
          query: { query: input, cap: !!obj.cap }
        });
      }
      // History
      const time = new Date().Format("yyyy-MM-dd hh:mm:ss");
      const stamp = obj.adv
        ? input.replace(/\(/g, "&L;").replace(/\)/g, "&R;")
        : input;
      const keyName = "history*" + stamp;
      if (!VueCookies.isKey(keyName)) {
        VueCookies.set(keyName, { query: input, time: time }, "3d");
      } else {
        VueCookies.remove(keyName);
        VueCookies.set(keyName, { query: input, time: time }, "3d");
      }
    }
  },
  actions: {},
  modules: {}
});
