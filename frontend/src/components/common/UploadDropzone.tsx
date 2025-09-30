import { IconTableImport, IconUpload, IconX } from '@tabler/icons-react';
import { Group, Text } from '@mantine/core';
import { Dropzone, DropzoneProps, FileRejection } from '@mantine/dropzone';

const CSV_LIKE_TYPE = [
  'text/csv',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
];

interface UploadDropzoneProps extends Partial<DropzoneProps> {
  onFileAccepted: (file: File) => void;
  onFileRejected?: (fileRejections: FileRejection[]) => void;
}

export function UploadDropzone({ onFileAccepted, onFileRejected, ...props }: UploadDropzoneProps) {
  return (
    <Dropzone
      onDrop={(files) => {
        if (files[0]) onFileAccepted(files[0]);
      }}
      onReject={onFileRejected}
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
