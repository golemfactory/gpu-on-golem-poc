import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { RootState } from 'store';

const initialState: number | undefined = 0;

export const errorSlice = createSlice({
  name: 'error',
  initialState,
  reducers: {
    setError: (state, action: PayloadAction<number>) => action.payload,
    resetError: () => initialState,
  },
});

export const { setError, resetError } = errorSlice.actions;

export const selectError = (state: RootState) => state.error;

export default errorSlice;
