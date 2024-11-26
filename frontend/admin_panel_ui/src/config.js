// export const config = {
//   apiUrl: import.meta.env.VITE_API_URL
// }

export const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? import.meta.env.VITE_API_URL
    : '/api'  // This will use the proxy in development
}