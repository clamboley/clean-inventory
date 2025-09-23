// frontend/src/pages/Dashboard.page.tsx
import { IconTableImport, IconUpload, IconX } from '@tabler/icons-react';
import { Group, Text } from '@mantine/core';
import { Dropzone, DropzoneProps } from '@mantine/dropzone';
import { showNotification } from '@mantine/notifications';
import { AppLayout } from '../../components/layout/AppLayout';

const CSV_LIKE_TYPE = [
  'text/csv',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
];

function UploadExample(props: Partial<DropzoneProps>) {
  async function handleUpload(files: File[]) {
    const file = files[0];
    if (!file) return;

    const fd = new FormData();
    fd.append('file', file);

    try {
      const resp = await fetch('http://localhost:8000/api/items/import', {
        method: 'POST',
        body: fd,
      });

      if (!resp.ok) {
        const text = await resp.text();
        showNotification({
          title: 'Upload failed',
          message: `Server error: ${resp.status} ${text}`,
          color: 'red',
        });
        return;
      }

      const data = await resp.json();
      const createdCount = data.created?.length ?? 0;
      const errorCount = data.errors?.length ?? 0;

      showNotification({
        title: 'Import complete',
        message: `${createdCount} items created, ${errorCount} rows had errors.`,
        color: errorCount > 0 ? 'yellow' : 'green',
      });

      // Optionally: log details to console or display on UI
      console.log('Import result:', data);
    } catch (err) {
      console.error('Import failed', err);
      showNotification({
        title: 'Upload error',
        message: String(err),
        color: 'red',
      });
    }
  }

  return (
    <Dropzone
      onDrop={(files) => handleUpload(files)}
      onReject={(files) => {
        console.log('rejected files', files);
        showNotification({
          title: 'Rejected file',
          message: 'Unsupported file type or too large',
          color: 'red',
        });
      }}
      maxSize={5 * 1024 ** 2}
      accept={CSV_LIKE_TYPE}
      {...props}
    >
      <Group justify="center" gap="xl" mih={220} style={{ pointerEvents: 'none' }}>
        <Dropzone.Accept>
          <IconUpload size={52} color="var(--mantine-color-blue-6)" stroke={1.5} />
        </Dropzone.Accept>
        <Dropzone.Reject>
          <IconX size={52} color="var(--mantine-color-red-6)" stroke={1.5} />
        </Dropzone.Reject>
        <Dropzone.Idle>
          <IconTableImport size={52} color="var(--mantine-color-dimmed)" stroke={1.5} />
        </Dropzone.Idle>

        <div>
          <Text size="xl" inline>
            Import items from a file
          </Text>
          <Text size="sm" c="dimmed" inline mt={7}>
            Format: .csv, .xlsx or .xls
          </Text>
        </div>
      </Group>
    </Dropzone>
  );
}
export function DashboardPage() {
  return (
    <AppLayout>
      <UploadExample />
    </AppLayout>
  );
}
