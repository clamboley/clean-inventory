import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { DashboardPage } from './pages/Dashboard/Dashboard.page';
import { HomePage } from './pages/Home/Home.page';
import { InventoryPage } from './pages/Inventory/Inventory.page';
import { NotFoundPage } from './pages/NotFound.page';

const router = createBrowserRouter([
  { path: '/', element: <HomePage /> },
  { path: '/dashboard', element: <DashboardPage /> },
  { path: '/inventory', element: <InventoryPage /> },
  { path: '*', element: <NotFoundPage /> },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
