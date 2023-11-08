//vite.config.js
import { defineConfig } from "vite";
import { djangoVitePlugin } from "django-vite-plugin";

export default defineConfig({
  plugins: [
    djangoVitePlugin({
      input: ["./static/js/main.js", "./static/styles/tailwind.css"],
    }),
  ],
});
