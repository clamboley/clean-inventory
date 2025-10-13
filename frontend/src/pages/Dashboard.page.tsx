import { SimpleGrid, Skeleton } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { DownloadZone } from '../components/common/DownloadAllZone';
import { UploadDropzone } from '../components/common/UploadDropzone';
import { AppLayout } from '../components/layout/AppLayout';
import { ImportItemsResponse } from '../models/item';
import { uploadItems } from '../services/items.service';

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
      <SimpleGrid
        cols={3}
        spacing="lg"
      >
        <Skeleton />
        <Skeleton />
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

        <Skeleton />
        <Skeleton />
        <DownloadZone />
      </SimpleGrid>
    </AppLayout>
  );
}
