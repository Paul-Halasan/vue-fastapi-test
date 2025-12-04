import axios from 'axios'

// adjust baseURL kung may backend domain ka na
const api = axios.create({
  baseURL: 'https://isaac-fifth-cdt-sauce.trycloudflare.com',
})

// Products
export const getProducts = () => api.get('/products')
export const createProduct = (data) => api.post('/products', data)
export const updateProduct = (id, data) => api.patch(`/products/${id}`, data)
export const deleteProduct = (id) => api.delete(`/products/${id}`)

// Materials
export const getMaterials = () => api.get('/materials')
export const createMaterial = (data) => api.post('/materials', data)
export const updateMaterial = (id, data) => api.patch(`/materials/${id}`, data)
export const deleteMaterial = (id) => api.delete(`/materials/${id}`)

// Product-Materials
export const addProductMaterial = (data) => api.post('/product-materials', data)
export const updateProductMaterial = (id, data) => api.patch(`/product-materials/${id}`, data)
export const deleteProductMaterial = (id) => api.delete(`/product-materials/${id}`)
