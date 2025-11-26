<template>
  <div class="glassmorphism-container" style="margin: 2rem 1rem; padding: 1rem; border-radius: 15px;">
    <div class="header-section">

      <h1 class="page-title">Products</h1>

      <div class="controls-section">
        <n-popover trigger="hover">
          <template #trigger>
            <n-button
              strong
              round
              color="#f472b6"
              style="--n-color-hover: #f472b6; --n-color-pressed: #db2777"
              @click="showAddProductModal = true"
              class="add-button"
            >
              Add Product
            </n-button>
          </template>
          <span>Click mo lang to sya pag mag-add ka na ng products.</span>
        </n-popover>

        <!-- eslint-disable-next-line vue/no-v-model-argument -->
        <n-input v-model:value="searchQuery"
          type="text"
          size="medium"
          placeholder="Search for item name..."
          round
          class="search-input"
          @input="handleSearch"
        />
      </div>

    </div>

    <!-- Modal moved outside of popover -->
    <!-- eslint-disable-next-line vue/no-v-model-argument -->
    <n-modal v-model:show="showAddProductModal">
      <n-card class="glassmorphism-modal modal-responsive">
        <template #header>Add New Product</template>

        <n-form>
          <n-form-item label="Product Name">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="form.product_name" placeholder="Enter product name" />
          </n-form-item>

          <n-form-item label="Selling Price">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input-number v-model:value="form.selling_price" min="0" :show-button="false" />
          </n-form-item>

          <n-form-item label="Materials Used">
            <div style="display: flex; flex-direction: column; gap: 12px;">
              <div v-for="(material, index) in form.materials" :key="index" style="padding: 15px; border: 1px solid #ffc0e0; border-radius: 8px; background: #fff5f9;">
                <n-space align="center">
                  <!-- Material Selection -->
                  <n-select
                    v-model="material.material_id"
                    :options="materialOptions"
                    placeholder="Select material..."
                    style="width: 350px;"
                    @update:value="updateMaterialPrice(index, $event)"
                  />

                  <!-- Quantity Input -->
                  <n-input-number
                    v-model="material.quantity"
                    min="1"
                    step="1.0"
                    placeholder="Qty"
                    style="width: 100px;"
                    @update:value="onQuantityChange(index, $event)"
                    :show-button="false"
                  />

                  <!-- Material Unit Badge -->
                  <span v-if="material.material_unit" style="color: #ff5eae; font-weight: 500;">
                    {{ material.material_unit }}
                  </span>

                  <!-- Price per unit display -->
                  <span v-if="material.price" style="color: #ff5eae; font-weight: 500;">
                    ₱ {{ material.price.toFixed(2) }} / unit
                  </span>

                  <!-- Subtotal -->
                  <span v-if="material.price && material.quantity" style="color: #ff67b3; font-weight: 600;">
                  = ₱ {{ (material.price * material.quantity).toFixed(2) }}
                  </span>

                  <!-- Remove button -->
                  <n-button
                    @click="removeMaterial(index)"
                    type="error"
                    size="small"
                    circle
                    v-if="form.materials.length > 1"
                  >
                    ✕
                  </n-button>
                </n-space>
              </div>
            </div>
          </n-form-item>

          <!-- Add Material Button - moved outside form-item -->
          <div style="margin-bottom: 16px;">
            <n-button
              @click="addMaterial"
              dashed
              style="width: 100%; border: 1px dashed #fff5f9; color: #ff67b3; background-color: #fff5f9;"
              :disabled="!canAddMaterial"
            >
              <template v-if="!canAddMaterial">
                ⚠️ Enter quantities first
              </template>
              <template v-else>
                + Add Material
              </template>
            </n-button>
          </div>

          <n-divider />

          <!-- Real-time Computations and Buttons Side by Side -->
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
            <!-- Left: Real-time Computations -->
            <n-space vertical style="flex: 1;">
              <div><b>Total Cost:</b> ₱{{ totalCost.toFixed(2) }}</div>
              <div><b>Suggested Price (×3.3):</b> ₱{{ suggestedPrice.toFixed(2) }}</div>
              <div><b>Profit:</b> ₱{{ profit.toFixed(2) }}</div>
              <div><b>Profit Margin:</b> {{ profitMargin.toFixed(2) }}%</div>
            </n-space>

            <!-- Right: Action Buttons -->
            <n-space style="flex-shrink: 0;">
              <n-button @click="cancelAddProduct" size="large">
                Cancel
              </n-button>
              <n-button
                type="secondary"
                @click="submitProduct"
                size="large"
                :disabled="!canSubmitProduct"
              >
                Add Product
              </n-button>
            </n-space>
          </div>
        </n-form>
      </n-card>
    </n-modal>

    <!-- Edit Product Modal -->
    <!-- eslint-disable-next-line vue/no-v-model-argument -->
    <n-modal v-model:show="showEditProductModal">
      <n-card class="glassmorphism-modal modal-responsive-small">
        <template #header>Edit Product: {{ editingProduct?.product_name }}</template>

        <n-form>
          <n-form-item label="Product Name">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="editForm.product_name" placeholder="Enter product name" />
          </n-form-item>

          <n-form-item label="Selling Price">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input-number v-model:value="editForm.selling_price" min="0" :show-button="false" />
          </n-form-item>

          <n-form-item label="Materials Used">
            <div style="display: flex; flex-direction: column; gap: 12px;">
              <div v-for="(material, index) in editForm.materials" :key="`edit-${index}-${material.material_id || 'new'}`" style="padding: 15px; border: 1px solid #ffc0e0; border-radius: 8px; background: #fff5f9;">
                <n-space align="center">
                  <!-- Material Selection -->
                  <!-- eslint-disable-next-line vue/no-v-model-argument -->
                  <n-select v-model:value="material.material_id"
                    :options="materialOptions"
                    placeholder="Select material..."
                    style="width: 250px;"
                    @update:value="updateEditMaterialPrice(index, $event)"
                  />

                  <!-- Quantity Input -->
                  <!-- eslint-disable-next-line vue/no-v-model-argument -->
                  <n-input-number v-model:value="material.quantity"
                    min="1"
                    step="1.0"
                    placeholder="Qty"
                    style="width: 80px;"
                    @update:value="onEditQuantityChange(index, $event)"
                    :show-button="false"
                  />

                  <!-- Material Unit Badge -->
                  <span v-if="material.material_unit" style="color: #ff5eae; font-weight: 500;">
                    {{ material.material_unit }}
                  </span>

                  <!-- Price per unit display -->
                  <span v-if="material.price" style="color: #ff5eae; font-weight: 500;">
                    ₱ {{ material.price.toFixed(2) }} / unit
                  </span>

                  <!-- Subtotal -->
                  <span v-if="material.price && material.quantity" style="color: #ff67b3; font-weight: 600;">
                  = ₱ {{ (material.price * material.quantity).toFixed(2) }}
                  </span>

                  <!-- Remove button -->
                  <n-button
                    @click="removeEditMaterial(index)"
                    type="error"
                    size="small"
                    circle
                    v-if="editForm.materials.length > 1"
                  >
                    ✕
                  </n-button>
                </n-space>
              </div>
            </div>
          </n-form-item>

          <!-- Add Material Button -->
          <div style="margin-bottom: 16px;">
            <n-button
              @click="addEditMaterial"
              dashed
              style="width: 100%; border: 1px dashed #ffc0e0; color: #ff5eae;"
              :disabled="!canAddEditMaterial"
            >
              <template v-if="!canAddEditMaterial">
                ⚠️ Enter quantities first
              </template>
              <template v-else>
                + Add Material
              </template>
            </n-button>
          </div>

          <n-divider />

          <!-- Product Info Display -->
          <div style="margin-bottom: 16px; padding: 12px; background: #fff0f7; border-radius: 8px;">
            <h4 style="margin: 0 0 8px 0; color: #ff5eae;">Current Product Info:</h4>
            <div><b>Total Cost (Live):</b> ₱{{ editTotalCost.toFixed(2) }}</div>
            <div><b>Current Profit:</b> ₱{{ (editForm.selling_price - editTotalCost).toFixed(2) }}</div>
            <div><b>Current Margin:</b> {{ editTotalCost > 0 ? ((editForm.selling_price - editTotalCost) / editTotalCost * 100).toFixed(2) : '0.00' }}%</div>
          </div>

          <!-- Action Buttons -->
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 20px;">
            <!-- Left: Change indicator -->
            <div style="flex: 1;">
              <span v-if="hasChanges" style="color: #ff67b3; font-weight: 600;">
                ⚠️ You have unsaved changes
              </span>
            </div>

            <!-- Right: Action Buttons -->
            <n-space style="flex-shrink: 0;">
              <n-button
                @click="deleteProductFromModal"
                type="error"
                size="large"
                style="background-color: #dc3545; border-color: #dc3545; color: white"
              >
                Delete Product
              </n-button>
              <n-button @click="showEditProductModal = false" size="large">
                Cancel
              </n-button>
              <n-button
                style="background-color: #ff67b3; color: white"
                @click="saveProductChanges"
                size="large"
                :disabled="!hasChanges || !editForm.product_name.trim() || editForm.selling_price <= 0"
              >
                Save Changes
              </n-button>
            </n-space>
          </div>
        </n-form>
      </n-card>
    </n-modal>


    <n-data-table
      class="pinkTable"
      :columns="columns"
      :data="products"
      :loading="loading"
      :bordered="true"
      striped
      :scroll-x="1200"
      :max-height="500"
      virtual-scroll
    />
  </div>
</template>


<script setup>
import { ref, onMounted, computed, watch, h, nextTick } from "vue"
import axios from "axios"

// API base URL (palitan kung iba yung gamit mo)
const API_BASE = "https://adoption-applies-wanna-civil.trycloudflare.com"

const products = ref([])
const allProducts = ref([]) // Store all products for filtering
const loading = ref(false)
const searchQuery = ref(null)
const showAddProductModal = ref(false)
const showEditProductModal = ref(false)
const editingProduct = ref(null)
const hasChanges = ref(false)

// Form data
const form = ref({
  product_name: '',
  selling_price: 0,
  materials: [
    { material_id: null, quantity: 0, price: 0 }
  ]
})

// Edit form data
const editForm = ref({
  product_name: '',
  selling_price: 0,
  materials: []
})

const originalEditForm = ref({
  product_name: '',
  selling_price: 0,
  materials: []
})

// Materials data
const materialOptions = ref([])

// Computed properties for calculations
const totalCost = computed(() => {
  const cost = form.value.materials.reduce((sum, mat) => {
    const materialCost = (mat.price || 0) * (mat.quantity || 0)
    return sum + materialCost
  }, 0)
  console.log('Total cost updated:', cost)
  return cost
})

const suggestedPrice = computed(() => {
  const suggested = totalCost.value * 3.3
  console.log('Suggested price updated:', suggested)
  return suggested
})

const profit = computed(() => {
  const profitValue = (form.value.selling_price || 0) - totalCost.value
  console.log('Profit updated:', profitValue)
  return profitValue
})

const profitMargin = computed(() => {
  if (totalCost.value === 0) return 0
  // Correct profit margin formula: ((selling_price - total_cost) / total_cost) * 100
  const margin = (((form.value.selling_price || 0) - totalCost.value) / totalCost.value) * 100
  // Cap at 999999.99 to prevent database overflow (DECIMAL(8,2) limit)
  const cappedMargin = Math.min(Math.max(margin, -999999.99), 999999.99)
  console.log('Profit margin updated:', cappedMargin)
  return cappedMargin
})

// Validation computed properties
const canAddMaterial = computed(() => {
  // Check if all existing materials have quantities > 0
  return form.value.materials.every(material =>
    material.quantity && material.quantity > 0
  )
})

const canSubmitProduct = computed(() => {
  // Check if product name is filled and at least one material with quantity
  const hasProductName = form.value.product_name && form.value.product_name.trim() !== ''
  const hasValidMaterials = form.value.materials.some(material =>
    material.material_id && material.quantity && material.quantity > 0
  )
  const hasSellingPrice = form.value.selling_price && form.value.selling_price > 0

  return hasProductName && hasValidMaterials && hasSellingPrice
})

// Functions
const cancelAddProduct = () => {
  // Reset form to initial state
  form.value = {
    product_name: '',
    selling_price: 0,
    materials: [
      { material_id: null, quantity: 0, price: 0 }
    ]
  }
  showAddProductModal.value = false
}

const addMaterial = () => {
  form.value.materials.push({ material_id: null, quantity: 0, price: 0 })
}

const removeMaterial = (index) => {
  if (form.value.materials.length > 1) {
    form.value.materials.splice(index, 1)
  }
}

const updateMaterialPrice = (index, materialId) => {
  const selectedMaterial = materialOptions.value.find(mat => mat.value === materialId)
  if (selectedMaterial) {
    // Update all material details and ensure reactivity
    form.value.materials[index].price = selectedMaterial.price
    form.value.materials[index].material_id = materialId
    form.value.materials[index].material_name = selectedMaterial.material_name
    form.value.materials[index].material_type = selectedMaterial.material_type
    form.value.materials[index].material_unit = selectedMaterial.material_unit

    // Force reactivity by creating a new array reference
    form.value.materials = [...form.value.materials]

    console.log('Material updated:', {
      index,
      materialId,
      price: selectedMaterial.price,
      type: selectedMaterial.material_type,
      materials: form.value.materials
    })
  }
}

const onQuantityChange = (index, newQuantity) => {
  form.value.materials[index].quantity = newQuantity || 0

  // Force reactivity by creating a new array reference
  form.value.materials = [...form.value.materials]

  console.log('Quantity updated:', {
    index,
    newQuantity,
    materials: form.value.materials
  })
}

const submitProduct = async () => {
  console.log('dito ko pinoporma kung pano sa schema sa backend:', {
    product_name: form.value.product_name,
    selling_price: form.value.selling_price,
    materials: form.value.materials.map(mat => ({
      material_id: mat.material_id,
      quantity_used: mat.quantity
    })),
  })

  try {
    await axios.post(`${API_BASE}/products`, {
      product_name: form.value.product_name,
      selling_price: form.value.selling_price,
      total_cost: totalCost.value,
      materials: form.value.materials.map(mat => ({
        material_id: mat.material_id,
        quantity_used: mat.quantity
      })),
    })
  } catch (err) {
    console.error("Failed to submit product:", err)
    return
  }

  // Reset form
  form.value = {
    product_name: '',
    selling_price: 0,
    materials: [
      { material_id: null, quantity: 0, price: 0 }
    ]
  }

  showAddProductModal.value = false
  console.log('Product added successfully')
  await fetchProducts()
}

const columns = [
  { title: "Name", key: "product_name", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Total Cost", key: "total_cost", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Suggested Price", key: "suggested_price", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Selling Price", key: "selling_price", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Profit", key: "profit", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Profit Margin (%)", key: "profit_margin", defaultSortOrder: 'ascend', sorter: 'default' },
  {
    title: "Actions",
    key: "actions",
    render(row) {
      return h('n-button', {
        size: 'small',
        type: 'info',
        onClick: () => openEditModal(row)
      }, { default: () => 'Edit' })
    }
  }
]

const fetchProducts = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/products`)
    allProducts.value = res.data
    products.value = res.data // Initially show all products
  } catch (err) {
    console.error("Failed to fetch products:", err)
  } finally {
    loading.value = false
  }
}

const fetchMaterials = async () => {
  try {
    const res = await axios.get(`${API_BASE}/materials`)
    console.log('Fetched materials from API:', res.data)
    materialOptions.value = res.data.map(mat => ({
      label: `[${mat.material_type}] ${mat.material_name}`,
      value: mat.material_id,
      price: mat.material_unit_price,
      material_name: mat.material_name,
      material_type: mat.material_type,
      material_unit: mat.material_unit
    }))
  } catch (err) {
    console.error("Failed to fetch materials:", err)
  }
}

const handleSearch = () => {
  console.log('Search input changed:', searchQuery.value)
  loading.value = true

  if (!searchQuery.value || searchQuery.value == '' || searchQuery.value == null) {
    products.value = allProducts.value
  }
  else {
    products.value = allProducts.value.filter(product =>
      product.product_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  loading.value = false
  return
}

onMounted(() => {
  fetchProducts()
  fetchMaterials()
})

// Watch for form changes to ensure reactivity
watch(() => form.value.materials, (newMaterials) => {
  console.log('Materials changed:', newMaterials)
}, { deep: true })

watch(() => form.value.selling_price, (newPrice) => {
  console.log('Selling price changed:', newPrice)
})

// Edit material management functions
const addEditMaterial = () => {
  editForm.value.materials.push({
    material_id: null,
    quantity: 0,
    price: 0,
    pm_id: null // No PM ID for new materials
  })
}

const removeEditMaterial = (index) => {
  if (editForm.value.materials.length > 1) {
    editForm.value.materials.splice(index, 1)
  }
}

const updateEditMaterialPrice = (index, materialId) => {
  const selectedMaterial = materialOptions.value.find(mat => mat.value === materialId)
  if (selectedMaterial) {
    editForm.value.materials[index].price = selectedMaterial.price
    editForm.value.materials[index].material_id = materialId
    editForm.value.materials[index].material_name = selectedMaterial.material_name
    editForm.value.materials[index].material_type = selectedMaterial.material_type
    editForm.value.materials[index].material_unit = selectedMaterial.material_unit

    // Force reactivity
    editForm.value.materials = [...editForm.value.materials]
  }
}

const onEditQuantityChange = (index, newQuantity) => {
  editForm.value.materials[index].quantity = newQuantity || 0
  // Force reactivity
  editForm.value.materials = [...editForm.value.materials]
}

// Computed properties for edit materials
const canAddEditMaterial = computed(() => {
  return editForm.value.materials.every(material =>
    material.quantity && material.quantity > 0
  )
})

// Computed for real-time total cost calculation in edit mode
const editTotalCost = computed(() => {
  return editForm.value.materials.reduce((sum, mat) => {
    return sum + ((mat.price || 0) * (mat.quantity || 0))
  }, 0)
})

// Edit functionality
const fetchProductMaterials = async (productId) => {
  try {
    console.log('Fetching materials for product ID:', productId)
    const res = await axios.get(`${API_BASE}/product-materials`)
    console.log('All product-materials from API:', res.data)

    const filtered = res.data.filter(pm => pm.product.product_id === productId)
    console.log('Filtered materials for this product:', filtered)

    const mapped = filtered.map(pm => ({
      material_id: pm.material.material_id,
      quantity: pm.quantity_used,
      price: pm.material.material_unit_price,
      material_name: pm.material.material_name,
      material_type: pm.material.material_type,
      material_unit: pm.material.material_unit,
      pm_id: pm.pm_id // Store the product-material relationship ID for updates/deletes
    }))

    console.log('Mapped materials for edit form:', mapped)
    return mapped
  } catch (err) {
    console.error('Failed to fetch product materials:', err)
    return []
  }
}

const openEditModal = async (product) => {
  editingProduct.value = product

  // Fetch materials for this product
  const productMaterials = await fetchProductMaterials(product.product_id)
  console.log('Fetched product materials:', productMaterials)

  // Ensure each material object is properly structured
  const processedMaterials = productMaterials.map(mat => ({
    material_id: mat.material_id,
    quantity: Number(mat.quantity) || 0,
    price: Number(mat.price) || 0,
    material_name: mat.material_name || '',
    material_type: mat.material_type || '',
    material_unit: mat.material_unit || '',
    pm_id: mat.pm_id
  }))

  editForm.value = {
    product_name: product.product_name,
    selling_price: product.selling_price,
    materials: processedMaterials
  }
  originalEditForm.value = {
    product_name: product.product_name,
    selling_price: product.selling_price,
    materials: JSON.parse(JSON.stringify(processedMaterials)) // Deep copy
  }

  console.log('Edit form set to:', editForm.value)
  console.log('Edit form materials:', editForm.value.materials)

  // Force reactivity update
  await nextTick()

  hasChanges.value = false
  showEditProductModal.value = true
}

// Watch editForm.materials for debugging
watch(() => editForm.value.materials, (newMaterials) => {
  console.log('Edit materials changed:', newMaterials)
}, { deep: true })

const saveProductChanges = async () => {
  try {
    // Step 1: Update basic product info
    await axios.patch(`${API_BASE}/products/${editingProduct.value.product_id}`, {
      product_name: editForm.value.product_name,
      selling_price: editForm.value.selling_price
    })

    // Step 2: Handle materials changes
    const currentMaterials = originalEditForm.value.materials
    const newMaterials = editForm.value.materials

    // Delete removed materials
    for (const currentMat of currentMaterials) {
      const stillExists = newMaterials.find(newMat => newMat.pm_id === currentMat.pm_id)
      if (!stillExists && currentMat.pm_id) {
        await axios.delete(`${API_BASE}/product-materials/${currentMat.pm_id}`)
        console.log(`Deleted material relationship: ${currentMat.pm_id}`)
      }
    }

    // Update existing materials or add new ones
    for (const newMat of newMaterials) {
      if (newMat.pm_id) {
        // Update existing material quantity
        const originalMat = currentMaterials.find(m => m.pm_id === newMat.pm_id)
        if (originalMat && originalMat.quantity !== newMat.quantity) {
          await axios.patch(`${API_BASE}/product-materials/${newMat.pm_id}`, {
            quantity_used: newMat.quantity
          })
          console.log(`Updated material ${newMat.pm_id} quantity to ${newMat.quantity}`)
        }
      } else {
        // Add new material
        if (newMat.material_id && newMat.quantity > 0) {
          await axios.post(`${API_BASE}/product-materials`, {
            product_id: editingProduct.value.product_id,
            material_id: newMat.material_id,
            quantity_used: newMat.quantity
          })
          console.log(`Added new material ${newMat.material_id} with quantity ${newMat.quantity}`)
        }
      }
    }

    console.log('Product updated successfully')
    showEditProductModal.value = false
    await fetchProducts() // Refresh the products list
  } catch (err) {
    console.error('Failed to update product:', err)
    if (err.response) {
      console.error('Error response:', err.response.data)
      alert(`Failed to update product: ${err.response.data.detail}`)
    }
  }
}

const deleteProductFromModal = async () => {
  const productName = editingProduct.value.product_name
  const productId = editingProduct.value.product_id

  if (confirm(`Are you sure you want to delete "${productName}"? This action cannot be undone.`)) {
    try {
      await axios.delete(`${API_BASE}/products/${productId}`)
      console.log('Product deleted successfully')
      showEditProductModal.value = false // Close the modal first
      await fetchProducts() // Refresh the products list
    } catch (err) {
      console.error('Failed to delete product:', err)
      if (err.response) {
        console.error('Error response:', err.response.data)
        alert(`Failed to delete product: ${err.response.data.detail}`)
      }
    }
  }
}

// Watch for changes in edit form
watch(() => editForm.value, (newForm) => {
  const nameChanged = newForm.product_name !== originalEditForm.value.product_name
  const priceChanged = newForm.selling_price !== originalEditForm.value.selling_price

  // Check materials changes
  const materialsChanged = JSON.stringify(newForm.materials.map(m => ({
    material_id: m.material_id,
    quantity: m.quantity
  }))) !== JSON.stringify(originalEditForm.value.materials.map(m => ({
    material_id: m.material_id,
    quantity: m.quantity
  })))

  hasChanges.value = nameChanged || priceChanged || materialsChanged
}, { deep: true })
</script>

<style scoped>
/* 🌟 GLASSMORPHISM EFFECTS 🌟 */
.glassmorphism-container {
  /* From https://css.glass */
  background: rgba(255, 186, 222, 0.25);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(7.9px);
  -webkit-backdrop-filter: blur(7.9px);
  border: 1px solid rgba(255, 255, 255, 0.17);
}

/* COHESIVE PINK TABLE STYLING 💖 */

/* Table wrapper styling */
.pinkTable :deep(.n-data-table-wrapper) {
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #ffc0e0;
  box-shadow: 0 4px 12px rgba(255, 103, 179, 0.1);
  max-height: 500px;
}

/* Scrollbar styling for table */
.pinkTable :deep(.n-scrollbar-rail) {
  background-color: rgba(255, 192, 224, 0.2) !important;
}

.pinkTable :deep(.n-scrollbar-handle) {
  background-color: #ff67b3 !important;
  border-radius: 6px;
}

.pinkTable :deep(.n-scrollbar-handle:hover) {
  background-color: #ff85c1 !important;
}

/* Fixed header during scroll */
.pinkTable :deep(.n-data-table-thead) {
  position: sticky;
  top: 0;
  z-index: 10;
}

/* Table background */
.pinkTable :deep(.n-data-table) {
  background-color: #fff5f9 !important;
}

/* Header styling */
.pinkTable :deep(.n-data-table-thead .n-data-table-th) {
  background-color: #ff67b3 !important;
  color: #ffffff !important;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #ff85c1 !important;
  padding: 16px 12px;
}

/* Header hover effect */
.pinkTable :deep(.n-data-table-thead .n-data-table-th:hover) {
  background-color: #ff85c1 !important;
  transition: background-color 0.3s ease;
}

/* All table rows default */
.pinkTable :deep(.n-data-table-tbody .n-data-table-tr) {
  background-color: #ffffff !important;
  transition: all 0.3s ease;
}

/* Even rows (striped effect) */
.pinkTable :deep(.n-data-table-tbody .n-data-table-tr:nth-child(even)) {
  background-color: #fff0f7 !important;
}

/* Odd rows */
.pinkTable :deep(.n-data-table-tbody .n-data-table-tr:nth-child(odd)) {
  background-color: #ffffff !important;
}

/* Enhanced hover effect */
.pinkTable :deep(.n-data-table-tbody .n-data-table-tr:hover) {
  background-color: #ffe6f2 !important;
  transform: scale(1.01);
  box-shadow: 0 2px 8px rgba(255, 103, 179, 0.2) !important;
  border-left: 4px solid #ff67b3 !important;
}

/* Table cell styling */
.pinkTable :deep(.n-data-table-td) {
  color: #ff5eae !important;
  font-weight: 500;
  font-size: 14px;
  padding: 14px 12px;
  border-bottom: 1px solid #ffc0e0 !important;
  transition: all 0.3s ease;
}

/* Hover text color for cells */
.pinkTable :deep(.n-data-table-tbody .n-data-table-tr:hover .n-data-table-td) {
  color: #ff67b3 !important;
  font-weight: 600;
}

/* Border colors */
.pinkTable :deep(.n-data-table-th),
.pinkTable :deep(.n-data-table-td) {
  border-color: #ffc0e0 !important;
}

/* Loading state override */
.pinkTable :deep(.n-data-table--loading .n-data-table-tbody .n-data-table-tr) {
  background-color: #fff5f9 !important;
}

/* Empty state */
.pinkTable :deep(.n-empty) {
  color: #ff5eae !important;
}

/* Sorting indicators */
.pinkTable :deep(.n-data-table-th .n-data-table-sorter) {
  color: rgba(255, 255, 255, 0.8) !important;
}

.pinkTable :deep(.n-data-table-th .n-data-table-sorter:hover) {
  color: #ffffff !important;
}

/* 💖 GLOBAL PINK THEME OVERRIDE 💖 */

/* 🔹 Primary Color Variables Override */
:deep(.n-config-provider) {
  --n-primary-color: #ff67b3 !important;
  --n-primary-color-hover: #ff85c1 !important;
  --n-primary-color-pressed: #e91e63 !important;
  --n-primary-color-suppl: #ff99cc !important;
}

/* 🔹 Input Fields - Text inputs, number inputs */
:deep(.n-input .n-input__input-el) {
  border-color: #ffc0e0 !important;
  transition: all 0.3s ease;
}

:deep(.n-input:hover .n-input__input-el) {
  border-color: #ff85c1 !important;
  box-shadow: 0 0 0 2px rgba(255, 103, 179, 0.2) !important;
}

:deep(.n-input.n-input--focus .n-input__input-el) {
  border-color: #ff67b3 !important;
  box-shadow: 0 0 0 2px rgba(255, 103, 179, 0.3) !important;
}

/* 🔹 Input Number - Quantity inputs */
:deep(.n-input-number .n-input .n-input__input-el) {
  border-color: #ffc0e0 !important;
}

:deep(.n-input-number:hover .n-input .n-input__input-el) {
  border-color: #ff85c1 !important;
  box-shadow: 0 0 0 2px rgba(255, 103, 179, 0.2) !important;
}

:deep(.n-input-number.n-input-number--focus .n-input .n-input__input-el) {
  border-color: #ff67b3 !important;
  box-shadow: 0 0 0 2px rgba(255, 103, 179, 0.3) !important;
}

/* 🔹 Select Dropdown */
:deep(.n-select .n-base-selection) {
  border-color: #ffc0e0 !important;
  transition: all 0.3s ease;
}

:deep(.n-select:hover .n-base-selection) {
  border-color: #ff85c1 !important;
  box-shadow: 0 0 0 2px rgba(255, 103, 179, 0.2) !important;
}

:deep(.n-select.n-select--focus .n-base-selection) {
  border-color: #ff67b3 !important;
  box-shadow: 0 0 0 2px rgba(255, 103, 179, 0.3) !important;
}

/* 🔹 Select Options */
:deep(.n-base-select-menu .n-base-select-option:hover) {
  background-color: #fff0f7 !important;
  color: #ff5eae !important;
}

:deep(.n-base-select-menu .n-base-select-option.n-base-select-option--selected) {
  background-color: #ff67b3 !important;
  color: white !important;
}

/* 🔹 Primary Buttons */
:deep(.n-button.n-button--primary-type) {
  background-color: #ff67b3 !important;
  border-color: #ff67b3 !important;
  color: white !important;
}

:deep(.n-button.n-button--primary-type:hover) {
  background-color: #ff85c1 !important;
  border-color: #ff85c1 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 103, 179, 0.3) !important;
}

:deep(.n-button.n-button--primary-type:active) {
  background-color: #e91e63 !important;
  border-color: #e91e63 !important;
}

/* 🔹 Default/Secondary Buttons */
:deep(.n-button.n-button--primary-type) {
  border-color: #ffc0e0 !important;
  color: #f778b7 !important;
}

:deep(.n-button.n-button--secondary-type ) {
  border-color: #ff85c1 !important;
  background-color: #fff0f7 !important;
  color: #ff67b3 !important;
  transform: translateY(-1px);
}

:deep(.n-button.n-button--default-type:hover) {
  border-color: #ff85c1 !important;
  background-color: #fff0f7 !important;
  color: #ff67b3 !important;
  transform: translateY(-1px);
}

/* 🔹 Dashed Buttons */
:deep(.n-button.n-button--dashed-type) {
  border-color: #ffc0e0 !important;
  color: #ff5eae !important;
}

:deep(.n-button.n-button--dashed-type:hover) {
  border-color: #ff67b3 !important;
  background-color: #fff5f9 !important;
  color: #ff67b3 !important;
}

/* 🔹 Tags */
:deep(.n-tag.n-tag--info-type) {
  background-color: #ff67b3 !important;
  color: white !important;
  border: none !important;
}

/* 🔹 Modal */
:deep(.n-modal .n-card) {
  border: 2px solid #ffc0e0 !important;
}

:deep(.n-card .n-card__header) {
  border-bottom: 1px solid #ffc0e0 !important;
  color: #ff5eae !important;
}

/* 🔹 Form Items */
:deep(.n-form-item .n-form-item-label__text) {
  color: #ff5eae !important;
  font-weight: 600;
}

/* 🔹 Divider */
:deep(.n-divider) {
  border-color: #ffc0e0 !important;
}

/* 🔹 Disabled States */
:deep(.n-button.n-button--disabled) {
  background-color: #f8d7da !important;
  border-color: #f5c6cb !important;
  color: #721c24 !important;
  opacity: 0.6;
}

/* 📱 MOBILE RESPONSIVE STYLES 📱 */

/* Header Section */
.header-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  color: #ff5eae;
}

.controls-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.search-input {
  width: 250px;
  min-width: 200px;
}

.add-button {
  white-space: nowrap;
}

/* Modal Responsive Sizes */
.modal-responsive {
  width: 650px;
  max-width: 95vw;
  margin: 10px;
}

.modal-responsive-small {
  width: 500px;
  max-width: 95vw;
  margin: 10px;
}

/* Mobile First Approach */
@media (max-width: 768px) {
  .glassmorphism-container {
    margin: 1rem 0.5rem !important;
    padding: 0.75rem !important;
  }

  .header-section {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.25rem;
    text-align: center;
  }

  .controls-section {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .search-input {
    width: 100%;
    min-width: unset;
  }

  .add-button {
    width: 100%;
    justify-content: center;
  }

  /* Modal adjustments */
  .modal-responsive,
  .modal-responsive-small {
    width: 100%;
    max-width: calc(100vw - 20px);
    margin: 10px;
  }

  /* Table becomes horizontally scrollable */
  .pinkTable :deep(.n-data-table-wrapper) {
    max-height: 400px;
  }

  /* Adjust material form items for mobile */
  :deep(.n-space.n-space--align-center) {
    flex-wrap: wrap !important;
    gap: 8px !important;
  }

  /* Stack material form elements vertically on very small screens */
  :deep(.n-form-item) {
    margin-bottom: 12px;
  }

  /* Adjust button sizes */
  :deep(.n-button) {
    min-height: 44px; /* Touch-friendly size */
  }

  /* Real-time computations stack vertically */
  :deep(.n-space.n-space--vertical) {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .glassmorphism-container {
    margin: 0.5rem 0.25rem !important;
    padding: 0.5rem !important;
  }

  .page-title {
    font-size: 1.1rem;
  }

  /* Even smaller modal */
  .modal-responsive,
  .modal-responsive-small {
    width: 100%;
    max-width: calc(100vw - 10px);
    margin: 5px;
  }

  /* Stack computation and buttons vertically */
  :deep(.n-card__content > div:last-child) {
    flex-direction: column !important;
    gap: 15px !important;
  }

  /* Full-width action buttons */
  :deep(.n-space) {
    width: 100% !important;
    justify-content: stretch !important;
  }

  :deep(.n-space .n-button) {
    flex: 1 !important;
  }

  /* Table adjustments for very small screens */
  .pinkTable :deep(.n-data-table-wrapper) {
    max-height: 300px;
    font-size: 12px;
  }

  .pinkTable :deep(.n-data-table-td),
  .pinkTable :deep(.n-data-table-th) {
    padding: 8px 6px !important;
    font-size: 12px !important;
  }
}
</style>
