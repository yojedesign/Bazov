'use client';

import { useState, useCallback } from 'react';
import { Search } from 'lucide-react';
import { Input } from './input';

interface SearchBarProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  debounceMs?: number;
  className?: string;
}

export function SearchBar({
  placeholder = 'Search...',
  onSearch,
  debounceMs = 300,
  className = '',
}: SearchBarProps) {
  const [value, setValue] = useState('');
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = e.target.value;
      setValue(newValue);
      
      // Clear existing timeout
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      
      // Set new timeout for debounced search
      const newTimeoutId = setTimeout(() => {
        onSearch(newValue);
      }, debounceMs);
      
      setTimeoutId(newTimeoutId);
    },
    [onSearch, debounceMs, timeoutId]
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    onSearch(value);
  };

  const handleClear = () => {
    setValue('');
    onSearch('');
  };

  return (
    <form onSubmit={handleSubmit} className={`relative ${className}`}>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          className="pl-10 pr-10"
        />
        {value && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
          >
            ×
          </button>
        )}
      </div>
    </form>
  );
}
