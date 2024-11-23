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
        placeholder="Search by order number or customer..." 
        class="border p-2 rounded"
      />
      <select 
        v-model="statusFilter" 
        class="border p-2 rounded"
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
      >
        <option value="created_at">Sort by Date</option>
        <option value="order_number">Sort by Order Number</option>
        <option value="total_amount">Sort by Amount</option>
      </select>
      <input 
        type="date" 
        v-model="dateFilter"
        class="border p-2 rounded"
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
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="order in filteredOrders" :key="order.id">
            <td class="px-6 py-4 whitespace-nowrap font-medium">{{ order.order_number }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(order.created_at) }}</td>
            <td class="px-6 py-4">
              <div class="text-sm font-medium text-gray-900">{{ order.customer_name }}</div>
              <div class="text-sm text-gray-500">{{ order.customer_email }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">${{ formatAmount(order.total_amount) }}</td>
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
            <td class="px-6 py-4 whitespace-nowrap text-right space-x-2">
              <button 
                @click="editOrder(order)"
                class="text-indigo-600 hover:text-indigo-900"
              >
                Edit
              </button>
              <button 
                @click="updateStatus(order)"
                class="text-blue-600 hover:text-blue-900"
              >
                Update Status
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
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-medium mb-4">{{ editingOrder ? 'Edit Order' : 'Create Order' }}</h3>
        <form @submit.prevent="saveOrder">
          <div class="space-y-4">
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
              <label class="block text-sm font-medium text-gray-700">Customer Email</label>
              <input 
                v-model="orderForm.customer_email" 
                type="email" 
                required
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Total Amount</label>
              <input 
                v-model="orderForm.total_amount"
                type="number"
                step="0.01"
                min="0.01"
                required
                class="mt-1 block w-full border rounded-md shadow-sm p-2"
              />
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
                rows="3"
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
            <label class="block text-sm font-medium text-gray-700">Notes</label>
            <textarea 
              v-model="statusNote"
              class="mt-1 block w-full border rounded-md shadow-sm p-2"
              placeholder="Add a note about this status change..."
            ></textarea>
          </div>
          <div class="flex justify-end space-x-3">
            <button 
              @click="closeStatusModal"
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
    // State
    const orders = ref([])
    const searchQuery = ref('')
    const statusFilter = ref('all')
    const sortBy = ref('created_at')
    const dateFilter = ref('')
    const showAddModal = ref(false)
    const showStatusModal = ref(false)
    const editingOrder = ref(null)
    const selectedOrder = ref(null)
    const newStatus = ref('')
    const statusNote = ref('')

    const orderForm = ref({
      customer_name: '',
      customer_email: '',
      total_amount: '',
      status: 'pending',
      notes: ''
    })

    // Fetch orders
    const fetchOrders = async () => {
      try {
        const response = await axios.get('/api/orders/')
        orders.value = response.data
      } catch (error) {
        console.error('Error fetching orders:', error)
      }
    }

    const filteredOrders = computed(() => {
      let filtered = [...orders.value]

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(order => 
          order.order_number.toLowerCase().includes(query) ||
          order.customer_name.toLowerCase().includes(query) ||
          order.customer_email.toLowerCase().includes(query)
        )
      }

      if (statusFilter.value !== 'all') {
        filtered = filtered.filter(order => order.status === statusFilter.value)
      }

      if (dateFilter.value) {
        const filterDate = new Date(dateFilter.value).toISOString().split('T')[0]
        filtered = filtered.filter(order => 
          order.created_at.split('T')[0] === filterDate
        )
      }

      // Sorting
      filtered.sort((a, b) => {
        if (sortBy.value === 'created_at') {
          return new Date(b.created_at) - new Date(a.created_at)
        } else if (sortBy.value === 'total_amount') {
          return b.total_amount - a.total_amount
        } else {
          return a[sortBy.value].localeCompare(b[sortBy.value])
        }
      })

      return filtered
    })

    // Methods
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const formatAmount = (amount) => {
      return Number(amount).toFixed(2)
    }

    const editOrder = (order) => {
      editingOrder.value = order
      orderForm.value = { ...order }
      showAddModal.value = true
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
          notes: statusNote.value
        })
        await fetchOrders()
        closeStatusModal()
      } catch (error) {
        console.error('Error updating status:', error)
      }
    }

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

    const closeModal = () => {
      showAddModal.value = false
      editingOrder.value = null
      orderForm.value = {
        customer_name: '',
        customer_email: '',
        total_amount: '',
        status: 'pending',
        notes: ''
      }
    }

    const closeStatusModal = () => {
      showStatusModal.value = false
      selectedOrder.value = null
      newStatus.value = ''
      statusNote.value = ''
    }

    onMounted(fetchOrders)

    return {
      orders,
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
      formatDate,
      formatAmount,
      editOrder,
      updateStatus,
      submitStatusUpdate,
      saveOrder,
      deleteOrder,
      closeModal,
      closeStatusModal
    }
  }
}
</script>