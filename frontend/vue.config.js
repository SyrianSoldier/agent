const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    open: true,
    hot: true, 
    proxy: {
      "/api": {
        target: "http://localhost:1080", // 本地后端服务
        changeOrigin: true,
      }
    }
  }
})