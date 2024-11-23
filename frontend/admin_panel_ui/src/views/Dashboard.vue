<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium mb-4">Recent Products</h2>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <ul v-else class="divide-y divide-gray-200">
        <li v-for="product in products" :key="product.id" class="py-4">
          <div class="flex justify-between">
            <div class="">
              <p class="font-semibold">{{ product.name }}</p>
              <p class="text-sm text-gray-500">Stock: {{ product.stock }}</p>
            </div>
            <p class="text-sm font-medium text-gray-900">RM{{ product.price }}</p>
          </div>
        </li>
      </ul>
    </div>

    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium mb-4">Recent Orders</h2>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <ul v-else class="divide-y divide-gray-200">
        <li v-for="order in orders" :key="order.id" class="py-4">
          <div class="flex justify-between">
            <div>
              <p class="font-medium">Order #{{ order.order_number }}</p>
              <p class="text-sm text-gray-500">{{ order.status }}</p>
            </div>
            <p class="text-sm text-gray-500">{{ order.created_at }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const products = ref([])
    const orders = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchData = async () => {
      try {
        const [productsRes, ordersRes] = await Promise.all([
          axios.get('/api/products/'),
          axios.get('/api/orders/')
        ])
        products.value = productsRes.data.slice(0, 5) // Show only 5 recent products
        orders.value = ordersRes.data.slice(0, 5) // Show only 5 recent orders
      } catch (err) {
        error.value = 'Error loading data'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchData)

    return {
      products,
      orders,
      loading,
      error
    }
  }
}
</script>