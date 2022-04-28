function toJson(data) {
  const ans = isObject(data) ? data : new Function("return " + data)();
  return ans;
}

function isObject(obj) {
  return Object.prototype.toString.call(obj) == "[object Object]";
}

function cropVenue(acronym, full) {
  if (!acronym) {
    return full.length > 30 ? full.slice(0, 30) + "..." : full;
  } else {
    return acronym.length > 30 ? acronym.slice(0, 30) + "..." : acronym;
  }
}

export default {
  toJson,
  cropVenue
};
