import Vue from "vue";
import VueI18n from "vue-i18n";
import VueCookies from "vue-cookies";
import CHSLocale from "element-ui/lib/locale/lang/zh-CN";
import CHTLocale from "element-ui/lib/locale/lang/zh-TW";
import ENGLocale from "element-ui/lib/locale/lang/en";
import JPALocale from "element-ui/lib/locale/lang/ja";
import ElementLocale from "element-ui/lib/locale";

Vue.use(VueI18n);

function getNavigatorLanguage() {
  // Cookie
  if (VueCookies.isKey("locale")) {
    const locale = VueCookies.get("locale");
    if (["chs", "cht", "eng", "jpa"].includes(locale)) {
      return locale;
    }
  }
  // Navigator
  const lang = navigator.language.toLowerCase().substr(0, 2);
  const branch = navigator.language.toLowerCase().substr(3);
  switch (lang) {
    case "zh":
      switch (branch) {
        case "cn":
        case "sg":
          return "chs";
        case "hk":
        case "tw":
          return "cht";
      }
      return "chs";
    case "en":
      return "eng";
    case "ja":
      return "jpa";
    default:
      return "eng";
  }
}

const i18n = new VueI18n({
  locale: getNavigatorLanguage(),
  messages: {
    chs: Object.assign({}, require("@/lang/chs"), { ...CHSLocale }),
    cht: Object.assign({}, require("@/lang/cht"), { ...CHTLocale }),
    eng: Object.assign({}, require("@/lang/eng"), { ...ENGLocale }),
    jpa: Object.assign({}, require("@/lang/jpa"), { ...JPALocale })
  }
});

ElementLocale.i18n((key, value) => i18n.t(key, value));

export { i18n };
