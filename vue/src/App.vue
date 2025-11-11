<script setup>
import { NLayout, NLayoutHeader, NLayoutContent, NMenu } from 'naive-ui'
import { ref, h } from 'vue'
import { RouterView, useRouter } from 'vue-router'

const router = useRouter()

const menuOptions = [
  {
    label: () => h('span', 'Products'),
    key: 'products'
  },
  {
    label: () => h('span', 'Materials'),
    key: 'materials'
  }
]

const activeKey = ref('products')

function handleMenuClick(key) {
  activeKey.value = key
  router.push(`/${key}`)
}
</script>

<template>
  <n-layout class="app-layout" style="height: 100vh">
    <!-- Header -->
    <n-layout-header class="glassmorphism-header" bordered style="height: 64px; display: flex; align-items: center; padding: 0 24px;">
      <h2 class="app-title" style="margin: 0; flex: 1;">Inventory System</h2>
      <n-menu
        class="glassmorphism-menu"
        mode="horizontal"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuClick"
      />
    </n-layout-header>

    <!-- Content -->
    <n-layout-content class="glassmorphism-content" content-style="padding: 24px;">
      <router-view />
    </n-layout-content>
  </n-layout>
</template>

<style scoped>
/* 🌟 GLASSMORPHISM APP LAYOUT 🌟 */
.app-layout {
  /* Beautiful gradient background */
  background: linear-gradient(135deg,
    rgba(255, 182, 193, 0.3) 0%,
    rgba(255, 192, 203, 0.25) 25%,
    rgba(255, 228, 225, 0.2) 50%,
    rgba(255, 240, 245, 0.15) 75%,
    rgba(255, 255, 255, 0.1) 100%);
  min-height: 100vh;
  border: 1px solid rgba(255, 255, 255, 0.31);
}

.glassmorphism-header {
  /* From https://css.glass - Header glass effect */
  background: rgba(255, 192, 224, 0.2) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border: none !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 2px 20px rgba(255, 103, 179, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.31);
}

.app-title {
  color: #ff5eae !important;
  font-weight: 700;
  font-size: 1.5rem;
  text-shadow: 0 2px 10px rgba(255, 103, 179, 0.3);
  letter-spacing: 0.5px;
}

.glassmorphism-menu {
  background: rgba(255, 255, 255, 0.1) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(5px) !important;
  -webkit-backdrop-filter: blur(5px) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  padding: 4px !important;
}

.glassmorphism-content {
  /* Subtle glass background for content area */
  background: rgba(255, 245, 248, 0.1) !important;
  backdrop-filter: blur(2px) !important;
  -webkit-backdrop-filter: blur(2px) !important;
}

/* 🔹 Menu Item Styling */
:deep(.n-menu .n-menu-item) {
  color: #ff5eae !important;
  font-weight: 600;
  border-radius: 8px !important;
  margin: 0 4px !important;
  transition: all 0.3s ease !important;
}

:deep(.n-menu .n-menu-item:hover) {
  background: rgba(255, 103, 179, 0.15) !important;
  color: #ff67b3 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 103, 179, 0.2) !important;
}

:deep(.n-menu .n-menu-item.n-menu-item--selected) {
  background: rgba(255, 103, 179, 0.15) !important;
  color: #ff67b3 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 16px rgba(255, 103, 179, 0.25) !important;
  font-weight: 700;
  transition: all 0.3s ease !important;
}

/* 💖 Override Naive UI's default green active color */
:deep(.n-menu .n-menu-item.n-menu-item--selected .n-menu-item-content) {
  color: #ff5eae  !important;
}

:deep(.n-menu .n-menu-item.n-menu-item--selected .n-menu-item-content .n-menu-item-content__icon) {
  color: #ff67b3  !important;
}

:deep(.n-menu .n-menu-item.n-menu-item--selected span) {
  color: #ff67b3 !important;
}

/* Force pink color on all menu text elements */
:deep(.n-menu .n-menu-item *) {
  color: inherit !important;
}

/* 🔹 Menu Text Styling */
:deep(.n-menu .n-menu-item span) {
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 14px;
}

/* 🔹 Responsive Adjustments */
@media (max-width: 768px) {
  .glassmorphism-header {
    padding: 0 16px !important;
  }

  .app-title {
    font-size: 1.25rem;
  }

  .glassmorphism-menu {
    padding: 2px !important;
  }
}
</style>
