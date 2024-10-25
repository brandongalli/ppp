import axios, { AxiosInstance, AxiosResponse } from "axios";

const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJicmFuZG9uczFAZXhhbXBsZS5jb20iLCJleHAiOjE3MzAwNTMyNDB9.mJYNyr4Fcs4IsPNpBGT8C5MqxbYmoIUr1q1lMIhAvbk";

// Create an Axios instance with default settings
const api: AxiosInstance = axios.create({
  baseURL: "http://192.168.0.6:8000", // Replace with your API URL
  timeout: 10000, // Timeout in ms (optional)
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
});

// Handle response interceptor (optional, for logging or error handling)
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    console.error("API error:", error);
    return Promise.reject(error);
  }
);

export const getPlayerData = async (endpoint: string) => {
  const response = await api.get(endpoint);
  return response.data;
};

export const getGameData = async (endpoint: string) => {
  const response = await api.get(endpoint);
  return response.data;
};

export default api;
