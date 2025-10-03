import { notifications } from '@mantine/notifications';
import { UploadDropzone } from '../components/common/UploadDropzone';
import { AppLayout } from '../components/layout/AppLayout';
import { uploadItems } from '../services/items.service';
import { ImportItemsResponse } from '../models/item';

export function DashboardPage() {
  async function handleUpload(file: File) {
    try {
      const data: ImportItemsResponse = await uploadItems(file);

      const createdCount = data.created.length;
      const errorCount = data.errors.length;

      notifications.show({
        title: 'Import complete',
        message: `${createdCount} items created, ${errorCount} rows had errors.`,
        color: errorCount > 0 ? 'yellow' : 'green',
      });
    } catch (err) {
      notifications.show({
        title: 'Upload error',
        message: String(err),
        color: 'red',
      });
    }
  }

  return (
    <AppLayout>
      <UploadDropzone
        onFileAccepted={handleUpload}
        onFileRejected={() =>
          notifications.show({
            title: 'Rejected file',
            message: 'Unsupported file type or too large.',
            color: 'red',
          })
        }
      />
    </AppLayout>
  );
}
