type StatusType = 'NEW' | 'CHANGED' | 'UNCHANGED' | 'DELETED';

export function StatusBadge({ status }: { status: StatusType }) {
  const colors = {
    NEW: 'bg-blue-100 text-blue-800',
    CHANGED: 'bg-yellow-100 text-yellow-800',
    UNCHANGED: 'bg-green-100 text-green-800',
    DELETED: 'bg-red-100 text-red-800'
  } as const;

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
      {status}
    </span>
  );
}
  