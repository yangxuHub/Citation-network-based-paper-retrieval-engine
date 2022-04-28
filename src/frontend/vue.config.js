module.exports = {
  devServer: {
    port: 8080,
    proxy: {
      "/": {
        target: "http://10.108.17.104:5000",
        changeOrigin: true
      },
    }
  }
};
