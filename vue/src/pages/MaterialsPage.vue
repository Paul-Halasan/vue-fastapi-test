<template>
  <div class="glassmorphism-container" style="margin: 2rem 1rem; padding: 1rem; border-radius: 15px;">
    <div class="header-section">

      <h1 class="page-title">Materials</h1>

      <div class="controls-section">
        <n-popover trigger="hover">
          <template #trigger>
            <n-button
              strong
              round
              color="#f472b6"
              style="--n-color-hover: #f472b6; --n-color-pressed: #db2777"
              @click="showAddMaterialModal = true"
              class="add-button"
            >
              Add Material
            </n-button>
          </template>
          <span>Click mo lang to sya pag mag-add ka na ng materials.</span>
        </n-popover>

        <!-- eslint-disable-next-line vue/no-v-model-argument -->
        <n-input v-model:value="searchQuery"
          type="text"
          size="medium"
          placeholder="Search for material name..."
          round
          class="search-input"
          @input="handleSearch"
        />

        <input
          type="file"
          id="import-excel"
          accept=".xlsx, .xls"
          style="display: none;"
          @change="handleExcelUpload"
        />
        <button class="n-button n-button--primary-type" @click="triggerExcelUpload">
          Import Excel
        </button>
      </div>

    </div>

    <!-- Modal for Add Material -->
    <!-- eslint-disable-next-line vue/no-v-model-argument -->
    <n-modal v-model:show="showAddMaterialModal">
      <n-card class="glassmorphism-modal modal-responsive">
        <template #header>Add New Material</template>

        <n-form>
          <n-form-item label="Material Name">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="form.material_name" placeholder="Enter material name" />
          </n-form-item>

          <n-form-item label="Material Type">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="form.material_type" placeholder="Enter material type" />
          </n-form-item>

          <n-form-item label="Material Unit">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="form.material_unit" placeholder="e.g. kg, pieces, liters" />
          </n-form-item>

          <n-form-item label="Material Price">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input-number v-model:value="form.material_price" min="0" :show-button="false" placeholder="Total price" />
          </n-form-item>

          <n-form-item label="Material Quantity">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input-number v-model:value="form.material_quantity" min="1" :show-button="false" placeholder="Total quantity" />
          </n-form-item>

          <n-form-item label="Material Supplier (Optional)">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="form.material_supplier" placeholder="Enter supplier name" />
          </n-form-item>

          <n-divider />

          <!-- Real-time Computations and Buttons Side by Side -->
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
            <!-- Left: Real-time Computation -->
            <n-space vertical style="flex: 1;">
              <div><b>Unit Price:</b> ₱{{ unitPrice.toFixed(2) }}</div>
            </n-space>

            <!-- Right: Action Buttons -->
            <n-space style="flex-shrink: 0;">
              <n-button @click="cancelAddMaterial" size="large">
                Cancel
              </n-button>
              <n-button
                style="background-color: #fff5f9; color: white"
                @click="submitMaterial"
                size="large"
                :disabled="!canSubmitMaterial"
              >
                Add Material
              </n-button>
            </n-space>
          </div>
        </n-form>
      </n-card>
    </n-modal>

    <!-- Edit Material Modal -->
    <!-- eslint-disable-next-line vue/no-v-model-argument -->
    <n-modal v-model:show="showEditMaterialModal">
      <n-card class="glassmorphism-modal" style="width: 650px">
        <template #header>Edit Material: {{ editingMaterial?.material_name }}</template>

        <n-form>
          <n-form-item label="Material Name">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="editForm.material_name" placeholder="Enter material name" />
          </n-form-item>

          <n-form-item label="Material Type">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="editForm.material_type" placeholder="Enter material type" />
          </n-form-item>

          <n-form-item label="Material Unit">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="editForm.material_unit" placeholder="e.g. kg, pieces, liters" />
          </n-form-item>

          <n-form-item label="Material Price">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input-number v-model:value="editForm.material_price" min="0" :show-button="false" placeholder="Total price" />
          </n-form-item>

          <n-form-item label="Material Quantity">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input-number v-model:value="editForm.material_quantity" min="1" :show-button="false" placeholder="Total quantity" />
          </n-form-item>

          <n-form-item label="Material Supplier (Optional)">
            <!-- eslint-disable-next-line vue/no-v-model-argument -->
            <n-input v-model:value="editForm.material_supplier" placeholder="Enter supplier name" />
          </n-form-item>

          <n-divider />

          <!-- Real-time Computations -->
          <div style="margin-bottom: 16px; padding: 12px; background: #fff0f7; border-radius: 8px;">
            <h4 style="margin: 0 0 8px 0; color: #ff5eae;">Current Material Info:</h4>
            <div><b>Unit Price (Live):</b> ₱{{ editUnitPrice.toFixed(2) }}</div>
          </div>

          <!-- Action Buttons -->
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 20px;">
            <!-- Left: Change indicator -->
            <div style="flex: 1;">
              <span v-if="hasChanges" style="color: #ff67b3; font-weight: 600;">
                ⚠️ You have unsaved changes
              </span>
              <span v-if="editForm.material_price !== originalEditForm.material_price || editForm.material_quantity !== originalEditForm.material_quantity" style="color: #e91e63; font-weight: 600; display: block; margin-top: 4px;">
                🔄 Price changes will affect product costs!
              </span>
            </div>

            <!-- Right: Action Buttons -->
            <n-space style="flex-shrink: 0;">
              <n-button
                @click="deleteMaterialFromModal"
                type="error"
                size="large"
                style="background-color: #dc3545; border-color: #dc3545; color: white"
              >
                Delete Material
              </n-button>
              <n-button @click="showEditMaterialModal = false" size="large">
                Cancel
              </n-button>
              <n-button
                style="background-color: #ff67b3; color: white"
                @click="saveMaterialChanges"
                size="large"
                :disabled="!hasChanges || !editForm.material_name.trim() || editForm.material_price <= 0 || editForm.material_quantity <= 0"
              >
                Save Changes
              </n-button>
            </n-space>
          </div>
        </n-form>
      </n-card>
    </n-modal>

    <!-- Delete Warning Modal -->
    <!-- eslint-disable-next-line vue/no-v-model-argument -->
    <n-modal v-model:show="showDeleteWarningModal">
      <n-card class="glassmorphism-modal modal-responsive-small">
        <template #header>⚠️ Cannot Delete Material</template>

        <div style="margin-bottom: 16px;">
          <p style="color: #e91e63; font-weight: 600; margin-bottom: 12px;">
            This material cannot be deleted because it is being used by the following products:
          </p>

          <div style="background: #fff0f7; padding: 12px; border-radius: 8px; border-left: 4px solid #ff67b3;">
            <ul style="margin: 0; padding-left: 20px;">
              <li v-for="product in materialsInUse" :key="product" style="color: #ff5eae; margin-bottom: 4px;">
                <strong>{{ product }}</strong>
              </li>
            </ul>
          </div>

          <p style="color: #666; margin-top: 12px; font-size: 14px;">
            To delete this material, you must first remove it from all products that use it, or delete those products.
          </p>
        </div>

        <div style="display: flex; justify-content: flex-end;">
          <n-button @click="showDeleteWarningModal = false" type="secondary" size="large">
            Close
          </n-button>
        </div>
      </n-card>
    </n-modal>

    <n-data-table
      class="pinkTable"
      :columns="columns"
      :data="materials"
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
import { ref, onMounted, computed, watch, h } from "vue"
import axios from "axios"
import { NDataTable } from "naive-ui"
import * as XLSX from "xlsx"

// API base URL (palitan kung iba yung gamit mo)
const API_BASE = "https://isaac-fifth-cdt-sauce.trycloudflare.com"

const materials = ref([])
const allMaterials = ref([]) // Store all materials for filtering
const loading = ref(false)
const searchQuery = ref(null)
const showAddMaterialModal = ref(false)
const showEditMaterialModal = ref(false)
const showDeleteWarningModal = ref(false)
const editingMaterial = ref(null)
const materialsInUse = ref([])
const hasChanges = ref(false)

// Form data
const form = ref({
  material_name: '',
  material_type: '',
  material_unit: '',
  material_price: 0,
  material_quantity: 1,
  material_supplier: ''
})

// Edit form data
const editForm = ref({
  material_name: '',
  material_type: '',
  material_unit: '',
  material_price: 0,
  material_quantity: 1,
  material_supplier: ''
})

const originalEditForm = ref({
  material_name: '',
  material_type: '',
  material_unit: '',
  material_price: 0,
  material_quantity: 1,
  material_supplier: ''
})

// Computed properties for calculations
const unitPrice = computed(() => {
  if (form.value.material_quantity && form.value.material_quantity > 0) {
    return (form.value.material_price || 0) / form.value.material_quantity
  }
  return 0
})

// Validation computed properties
const canSubmitMaterial = computed(() => {
  const hasName = form.value.material_name && form.value.material_name.trim() !== ''
  const hasType = form.value.material_type && form.value.material_type.trim() !== ''
  const hasUnit = form.value.material_unit && form.value.material_unit.trim() !== ''
  const hasPrice = form.value.material_price && form.value.material_price > 0
  const hasQuantity = form.value.material_quantity && form.value.material_quantity > 0

  return hasName && hasType && hasUnit && hasPrice && hasQuantity
})

// Functions
const cancelAddMaterial = () => {
  // Reset form to initial state
  form.value = {
    material_name: '',
    material_type: '',
    material_unit: '',
    material_price: 0,
    material_quantity: 1,
    material_supplier: ''
  }
  showAddMaterialModal.value = false
}

const submitMaterial = async () => {
  console.log('dito ko pinoporma kung pano sa schema sa backend:', {
    material_name: form.value.material_name,
    material_type: form.value.material_type,
    material_unit: form.value.material_unit,
    material_price: form.value.material_price,
    material_quantity: form.value.material_quantity,
    material_unit_price: unitPrice.value,
    material_supplier: form.value.material_supplier
  })

  try {
    await axios.post(`${API_BASE}/materials`, {
      material_name: form.value.material_name,
      material_type: form.value.material_type,
      material_unit: form.value.material_unit,
      material_price: form.value.material_price,
      material_quantity: form.value.material_quantity,
      material_unit_price: unitPrice.value,
      material_supplier: form.value.material_supplier
    })

    // Reset form and refresh
    form.value = {
      material_name: '',
      material_type: '',
      material_unit: '',
      material_price: 0,
      material_quantity: 1,
      material_supplier: ''
    }
    showAddMaterialModal.value = false
    console.log("Material added successfully")
    await fetchMaterials()
  } catch (err) {
    console.error("Failed to submit material:", err)
  }
}

const columns = [
  { title: "Name", key: "material_name", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Type", key: "material_type", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Unit", key: "material_unit", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Price", key: "material_price", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Quantity", key: "material_quantity", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Unit Price", key: "material_unit_price", defaultSortOrder: 'ascend', sorter: 'default' },
  { title: "Supplier", key: "material_supplier", defaultSortOrder: 'ascend', sorter: 'default' },
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

const fetchMaterials = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/materials`)
    allMaterials.value = res.data
    materials.value = res.data // Initially show all materials
  } catch (err) {
    console.error("Failed to fetch materials:", err)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  console.log('Search input changed:', searchQuery.value)
  loading.value = true

  if (!searchQuery.value || searchQuery.value == '' || searchQuery.value == null) {
    materials.value = allMaterials.value
  }
  else {
    materials.value = allMaterials.value.filter(material =>
      material.material_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  loading.value = false
  return
}

onMounted(() => {
  fetchMaterials()
})

// Computed properties for edit materials
const editUnitPrice = computed(() => {
  if (editForm.value.material_quantity && editForm.value.material_quantity > 0) {
    return (editForm.value.material_price || 0) / editForm.value.material_quantity
  }
  return 0
})

// Validation computed properties for edit
// const canSaveMaterial = computed(() => {
//   const hasName = editForm.value.material_name && editForm.value.material_name.trim() !== ''
//   const hasType = editForm.value.material_type && editForm.value.material_type.trim() !== ''
//   const hasUnit = editForm.value.material_unit && editForm.value.material_unit.trim() !== ''
//   const hasPrice = editForm.value.material_price && editForm.value.material_price > 0
//   const hasQuantity = editForm.value.material_quantity && editForm.value.material_quantity > 0

//   return hasName && hasType && hasUnit && hasPrice && hasQuantity
// })

// Edit functionality
const openEditModal = (material) => {
  editingMaterial.value = material

  editForm.value = {
    material_name: material.material_name,
    material_type: material.material_type,
    material_unit: material.material_unit,
    material_price: material.material_price,
    material_quantity: material.material_quantity,
    material_supplier: material.material_supplier || ''
  }
  originalEditForm.value = {
    material_name: material.material_name,
    material_type: material.material_type,
    material_unit: material.material_unit,
    material_price: material.material_price,
    material_quantity: material.material_quantity,
    material_supplier: material.material_supplier || ''
  }

  hasChanges.value = false
  showEditMaterialModal.value = true
}

const saveMaterialChanges = async () => {
  try {
    await axios.patch(`${API_BASE}/materials/${editingMaterial.value.material_id}`, {
      material_name: editForm.value.material_name,
      material_type: editForm.value.material_type,
      material_unit: editForm.value.material_unit,
      material_price: editForm.value.material_price,
      material_quantity: editForm.value.material_quantity,
      material_supplier: editForm.value.material_supplier
    })

    console.log('Material updated successfully')
    showEditMaterialModal.value = false
    await fetchMaterials() // Refresh the materials list
  } catch (err) {
    console.error('Failed to update material:', err)
    if (err.response) {
      console.error('Error response:', err.response.data)
      alert(`Failed to update material: ${err.response.data.detail}`)
    }
  }
}

const deleteMaterialFromModal = async () => {
  // const materialName = editingMaterial.value.material_name
  const materialId = editingMaterial.value.material_id

  try {
    await axios.delete(`${API_BASE}/materials/${materialId}`)
    console.log('Material deleted successfully')
    showEditMaterialModal.value = false // Close the modal first
    await fetchMaterials() // Refresh the materials list
  } catch (err) {
    console.error('Failed to delete material:', err)
    if (err.response && err.response.data.detail) {
      // Check if it's the "material in use" error
      if (err.response.data.detail.products_using_material) {
        materialsInUse.value = err.response.data.detail.products_using_material
        showEditMaterialModal.value = false
        showDeleteWarningModal.value = true
      } else {
        alert(`Failed to delete material: ${err.response.data.detail}`)
      }
    }
  }
}

// Watch for changes in edit form
watch(() => editForm.value, (newForm) => {
  const nameChanged = newForm.material_name !== originalEditForm.value.material_name
  const typeChanged = newForm.material_type !== originalEditForm.value.material_type
  const unitChanged = newForm.material_unit !== originalEditForm.value.material_unit
  const priceChanged = newForm.material_price !== originalEditForm.value.material_price
  const quantityChanged = newForm.material_quantity !== originalEditForm.value.material_quantity
  const supplierChanged = newForm.material_supplier !== originalEditForm.value.material_supplier

  hasChanges.value = nameChanged || typeChanged || unitChanged || priceChanged || quantityChanged || supplierChanged
}, { deep: true })

const triggerExcelUpload = () => {
  document.getElementById("import-excel").click();
};

const handleExcelUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (e) => {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: "array" });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const jsonData = XLSX.utils.sheet_to_json(sheet);

    try {
      await axios.post(`${API_BASE}/materials/import`, jsonData);
      await fetchMaterials(); // Refresh materials list
      alert("Materials imported successfully!");
    } catch (error) {
      console.error("Failed to import materials:", error);
      alert("Failed to import materials. Please check the file format.");
    }
  };

  reader.readAsArrayBuffer(file);
};
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
  width: 550px;
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

  /* Adjust form elements for mobile */
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

  /* Warning modal specific adjustments */
  :deep(.n-card__content p) {
    font-size: 14px;
    line-height: 1.4;
  }

  :deep(.n-card__content ul) {
    font-size: 13px;
  }
}
</style>
