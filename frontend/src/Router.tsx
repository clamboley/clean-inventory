import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { DashboardPage } from './pages/Dashboard.page';
import { InventoryPage } from './pages/Inventory.page';
import { NotFoundPage } from './pages/NotFound.page';

const router = createBrowserRouter([
  { path: '/', element: <InventoryPage /> },
  { path: '/dashboard', element: <DashboardPage /> },
  { path: '*', element: <NotFoundPage /> },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
