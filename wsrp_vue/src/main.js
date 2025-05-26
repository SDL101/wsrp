import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";

import App from "./App.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import CustomerDashboard from "./components/CustomerDashboard.vue";
import UserProfile from "./components/UserProfile.vue";
import HomeScreen from "./components/HomeScreen.vue";
// import Dashboard from "./components/Dashboard.vue";
import DashboardLayout from "./layouts/DashboardLayout.vue";
import NewAccountPage from "./components/NewAccountPage.vue";
import TransferPage from "./components/TransferPage.vue";
//import CSRFVulnerableTransferPage from "./components/CSRFVulnerableTransferPage.vue";
import InstructionsPage from "./components/InstructionsPage.vue";
import FileUploadDemo from "./components/FileUploadDemo.vue";
import "./assets/main.css";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomeScreen }, // Show HomeScreen at root path
    { path: "/home", redirect: "/" }, // Redirect /home to root path
    { path: "/register", component: RegisterPage },
    { path: "/login", component: LoginPage },
    { path: "/adminDashboard", component: AdminDashboard },
    { path: "/customerDashboard", component: CustomerDashboard },
    { path: "/userProfile", component: UserProfile },
    { path: "/dashboard", component: DashboardLayout },
    { path: "/new-account", component: NewAccountPage },
    { path: "/csrf-vulnerable-transfer", component: TransferPage },
    { path: "/instructions", component: InstructionsPage },
    { path: "/file-upload-demo", component: FileUploadDemo },
  ],
});

// Use pinia for state management (isLoggedIn for one)
const pinia = createPinia();
const app = createApp(App);
app.use(pinia);
app.use(router);

app.mount("#app");
