<template>
  <div class="bg-white shadow rounded-lg p-6">
    <!-- Header with Add Order Button -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">Orders</h2>
      <button 
        @click="showAddModal = true"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Create Order
      </button>
    </div>

    <!-- Search and Filter Section -->
    <div class="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search orders..." 
        class="border p-2 rounded"
        @input="filterOrders"
      />
      <select 
        v-model="statusFilter" 
        class="border p-2 rounded"
        @change="filterOrders"
      >
        <option value="all">All Status</option>
        <option value="pending">Pending</option>
        <option value="processing">Processing</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
      <select 
        v-model="sortBy" 
        class="border p-2 rounded"
        @change="filterOrders"
      >
        <option value="date">Sort by Date</option>
        <option value="order_number">Sort by Order Number</option>
        <option value="status">Sort by Status</option>
      </select>
      <input 
        type="date" 
        v-model="dateFilter"
        class="border p-2 rounded"
        @change="filterOrders"
      />
    </div>

    <!-- Orders Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order #</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="order in filteredOrders" :key="order.id">
            <td class="px-6 py-4 whitespace-nowrap font-medium">{{ order.order_number }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(order.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ order.customer_details }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                :class="{
                  'px-2 py-1 rounded-full text-xs font-medium': true,
                  'bg-yellow-100 text-yellow-800': order.status === 'pending',
                  'bg-blue-100 text-blue-800': order.status === 'processing',
                  'bg-green-100 text-green-800': order.status === 'completed',
                  'bg-red-100 text-red-800': order.status === 'cancelled'
                }"
              >
                {{ order.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">${{ order.total }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right space-x-2">
              <button 
                @click="updateStatus(order)"
                class="text-blue-600 hover:text-blue-900"
              >
                Update Status
              </button>
              <button 
                @click="viewDetails(order)"
                class="text-green-600 hover:text-green-900"
              >
                View
              </button>
              <button 
                @click="deleteOrder(order.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Order Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-2xl">
        <h3 class="text-lg font-medium mb-4">{{ editingOrder ? 'Edit Order' : 'Create Order' }}</h3>
        <form @submit.prevent="saveOrder">
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Customer Name</label>
                <input 
                  v-model="orderForm.customer_name" 
                  type="text" 
                  required
                  class="mt-1 block w-full border rounded-md shadow-sm p-2"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Email</label>
                <input 
                  v-model="orderForm.email" 
                  type="email" 
                  required
                  class="mt-1 block w-full border rounded-md shadow-sm p-2"
                />
              </div>
            </div>
            
            <!-- Product Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Products</label>
              <div v-for="(item, index) in orderForm.items" :key="index" class="flex gap-2 mt-2">
                <select 
                  v-model="item.product_id"
                  class="flex-1 border rounded-md shadow-sm p-2"
                >
                  <option v-for="product in products" :key="product.id" :value="product.id">
                    {{ product.name }} - ${{ product.price }}
                  </option>
                </select>
                <input 
                  v-model="item.quantity"
                  type="number"
                  min="1"
                  class="w-24 border rounded-md shadow-sm p-2"
                />
                <button 
                  type="button"
                  @click="removeOrderItem(index)"
                  class="text-red-600 hover:text-red-900"
                >
                  Remove
                </button>
              </div>
              <button 
                type="button"
                @click="addOrderItem"
                class="mt-2 text-blue-600 hover:text-blue-900"
              >
                Add Product
              </button>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Status</label>
              <select 
                v-model="orderForm.status"
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              >
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Notes</label>
              <textarea 
                v-model="orderForm.notes"
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              ></textarea>
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
              {{ editingOrder ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Status Update Modal -->
    <div v-if="showStatusModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-medium mb-4">Update Order Status</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">New Status</label>
            <select 
              v-model="newStatus"
              class="mt-1 block w-full border rounded-md shadow-sm p-2"
            >
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Status Note</label>
            <textarea 
              v-model="statusNote"
              class="mt-1 block w-full border rounded-md shadow-sm p-2"
              placeholder="Add a note about this status change..."
            ></textarea>
          </div>
          <div class="flex justify-end space-x-3">
            <button 
              @click="showStatusModal = false"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button 
              @click="submitStatusUpdate"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Update Status
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const orders = ref([])
    const products = ref([])
    const searchQuery = ref('')
    const statusFilter = ref('all')
    const sortBy = ref('date')
    const dateFilter = ref('')
    const showAddModal = ref(false)
    const showStatusModal = ref(false)
    const editingOrder = ref(null)
    const selectedOrder = ref(null)
    const newStatus = ref('')
    const statusNote = ref('')

    const orderForm = ref({
      customer_name: '',
      email: '',
      items: [{ product_id: '', quantity: 1 }],
      status: 'pending',
      notes: ''
    })

    // Fetch data
    const fetchOrders = async () => {
      try {
        const response = await axios.get('/api/orders/')
        orders.value = response.data
      } catch (error) {
        console.error('Error fetching orders:', error)
      }
    }

    const fetchProducts = async () => {
      try {
        const response = await axios.get('/api/products/')
        products.value = response.data
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    }

    // Computed properties
    const filteredOrders = computed(() => {
      let filtered = [...orders.value]

      if (searchQuery.value) {
        filtered = filtered.filter(order => 
          order.order_number.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          order.customer_details.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      }

      if (statusFilter.value !== 'all') {
        filtered = filtered.filter(order => order.status === statusFilter.value)
      }

      if (dateFilter.value) {
        const filterDate = new Date(dateFilter.value)
        filtered = filtered.filter(order => {
          const orderDate = new Date(order.created_at)
          return orderDate.toDateString() === filterDate.toDateString()
        })
      }

      // Sorting
      filtered.sort((a, b) => {
        if (sortBy.value === 'date') {
          return new Date(b.created_at) - new Date(a.created_at)
        } else if (sortBy.value === 'order_number') {
          return a.order_number.localeCompare(b.order_number)
        } else if (sortBy.value === 'status') {
          return a.status.localeCompare(b.status)
        }
        return 0
      })

      return filtered
    })

    // Actions
    const saveOrder = async () => {
      try {
        if (editingOrder.value) {
          await axios.put(`/api/orders/${editingOrder.value.id}/`, orderForm.value)
        } else {
          await axios.post('/api/orders/', orderForm.value)
        }
        await fetchOrders()
        closeModal()
      } catch (error) {
        console.error('Error saving order:', error)
      }
    }

    const updateStatus = (order) => {
      selectedOrder.value = order
      newStatus.value = order.status
      showStatusModal.value = true
    }

    const submitStatusUpdate = async () => {
      try {
        await axios.patch(`/api/orders/${selectedOrder.value.id}/`, {
          status: newStatus.value,
          status_note: statusNote.value
        })
        await fetchOrders()
        showStatusModal.value = false
        selectedOrder.value = null
        newStatus.value = ''
        statusNote.value = ''
      } catch (error) {
        console.error('Error updating status:', error)
      }
    }

    const deleteOrder = async (id) => {
      if (confirm('Are you sure you want to delete this order?')) {
        try {
          await axios.delete(`/api/orders/${id}/`)
          await fetchOrders()
        } catch (error) {
          console.error('Error deleting order:', error)
        }
      }
    }

    const viewDetails = (order) => {
      // Implement order details view
      console.log('View order details:', order)
    }

    const addOrderItem = () => {
      orderForm.value.items.push({ product_id: '', quantity: 1 })
    }

    const removeOrderItem = (index) => {
      orderForm.value.items.splice(index, 1)
    }

    const closeModal = () => {
      showAddModal.value = false
      editingOrder.value = null
      orderForm.value = {
        customer_name: '',
        email: '',
        items: [{ product_id: '', quantity: 1 }],
        status: 'pending',
        notes: ''
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    // Initialize data on component mount
    onMounted(() => {
      fetchOrders()
      fetchProducts()
    })

    return {
      orders,
      products,
      searchQuery,
      statusFilter,
      sortBy,
      dateFilter,
      showAddModal,
      showStatusModal,
      editingOrder,
      orderForm,
      newStatus,
      statusNote,
      filteredOrders,
      saveOrder,
      updateStatus,
      deleteOrder,
      viewDetails,
      closeModal,
      formatDate,
      addOrderItem,
      removeOrderItem,
      submitStatusUpdate
    }
  }
}
</script>