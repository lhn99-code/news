import { useEffect } from 'react';

interface Props {
  message: string | null;
  onClear: () => void;
}

export function Toast({ message, onClear }: Props) {
  useEffect(() => {
    if (!message) return;
    const t = setTimeout(onClear, 2800);
    return () => clearTimeout(t);
  }, [message, onClear]);

  if (!message) return null;
  return <div className="toast">{message}</div>;
}
