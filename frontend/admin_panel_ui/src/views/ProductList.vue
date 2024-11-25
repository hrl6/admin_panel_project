<template>
  <div class="bg-white shadow rounded-lg p-6">
    <!-- Header with Add Product Button -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">Products</h2>
      <button 
        @click="showAddModal = true"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Add Product
      </button>
      <button 
        @click="testBackend"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Test testBackend
      </button>
    </div>
    
    <div v-if="response">Response: {{ response }}</div>
    <div v-if="error">Error: {{ error }}</div>
    <!-- Search and Filter Section -->
    <div class="mb-6 flex gap-4">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search products..." 
        class="border p-2 rounded flex-1"
        @input="filterProducts"
      />
      <select 
        v-model="stockFilter" 
        class="border p-2 rounded"
        @change="filterProducts"
      >
        <option value="all">All Stock</option>
        <option value="in">In Stock</option>
        <option value="low">Low Stock</option>
        <option value="out">Out of Stock</option>
      </select>
      <select 
        v-model="sortBy" 
        class="border p-2 rounded"
        @change="filterProducts"
      >
        <option value="name">Sort by Name</option>
        <option value="price">Sort by Price</option>
        <option value="stock">Sort by Stock</option>
      </select>
    </div>

    <!-- Products Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="product in filteredProducts" :key="product.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ product.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap">RM{{ product.price }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ product.stock }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                :class="{
                  'px-2 py-1 rounded-full text-xs font-medium': true,
                  'bg-green-100 text-green-800': product.stock > 10,
                  'bg-yellow-100 text-yellow-800': product.stock <= 10 && product.stock > 0,
                  'bg-red-100 text-red-800': product.stock === 0
                }"
              >
                {{ getStockStatus(product.stock) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              <button 
                @click="editProduct(product)"
                class="text-indigo-600 hover:text-indigo-900 mr-4"
              >
                Edit
              </button>
              <button 
                @click="deleteProduct(product.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Product Modal -->
    <div v-if="showAddModal || editingProduct" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-medium mb-4">{{ editingProduct ? 'Edit' : 'Add' }} Product</h3>
        <form @submit.prevent="saveProduct">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <input 
                v-model="productForm.name" 
                type="text" 
                required
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Description</label>
              <textarea 
                v-model="productForm.description" 
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              ></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Price</label>
              <input 
                v-model="productForm.price" 
                type="number" 
                step="0.01" 
                required
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Stock</label>
              <input 
                v-model="productForm.stock" 
                type="number" 
                required
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              />
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              type="button"
              @click="closeModal"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              {{ editingProduct ? 'Update' : 'Add' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// State
const products = ref([])
const searchQuery = ref('')
const stockFilter = ref('all')
const sortBy = ref('name')
const showAddModal = ref(false)
const editingProduct = ref(null)
const productForm = ref({
  name: '',
  description: '',
  price: 0,
  stock: 0
})

const response = ref(null)
const error = ref(null)
const testBackend = async () => {
  try {
    response.value = null
    error.value = null
    
    const resp = await fetch('https://adminpanelproject-production.up.railway.app/api/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await resp.json();
    response.value = data
    console.log('Response:', data);
  } catch (err) {
    error.value = err.message
    console.error('Error:', err);
  }
}
// Fetch products from API
const fetchProducts = async () => {
  try {
    const response = await axios.get('/api/products/')
    products.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

// Computed property for filtered and sorted products
const filteredProducts = computed(() => {
  let filtered = [...products.value]

  // Apply search filter
  if (searchQuery.value) {
    filtered = filtered.filter(product => 
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Apply stock filter
  switch (stockFilter.value) {
    case 'in':
      filtered = filtered.filter(product => product.stock > 10)
      break
    case 'low':
      filtered = filtered.filter(product => product.stock <= 10 && product.stock > 0)
      break
    case 'out':
      filtered = filtered.filter(product => product.stock === 0)
      break
  }

  // Apply sorting
  filtered.sort((a, b) => {
    if (sortBy.value === 'price') {
      return b.price - a.price
    } else if (sortBy.value === 'stock') {
      return b.stock - a.stock
    } else {
      return b.name.localeCompare(a.name)
    }
  })

  return filtered
})

// CRUD operations
const saveProduct = async () => {
  try {
    if (editingProduct.value) {
      await axios.put(`/api/products/${editingProduct.value.id}/`, productForm.value)
    } else {
      await axios.post('/api/products/', productForm.value)
    }
    await fetchProducts()
    closeModal()
  } catch (error) {
    console.error('Error saving product:', error)
  }
}

const editProduct = (product) => {
  editingProduct.value = product
  productForm.value = { ...product }
  showAddModal.value = true
}

const deleteProduct = async (id) => {
  if (confirm('Are you sure you want to delete this product?')) {
    try {
      await axios.delete(`/api/products/${id}/`)
      await fetchProducts()
    } catch (error) {
      console.error('Error deleting product:', error)
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  editingProduct.value = null
  productForm.value = {
    name: '',
    description: '',
    price: 0,
    stock: 0
  }
}

const getStockStatus = (stock) => {
  if (stock === 0) return 'Out of Stock'
  if (stock <= 10) return 'Low Stock'
  return 'In Stock'
}

// Lifecycle hook
onMounted(fetchProducts)
</script>