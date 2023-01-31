import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { RootState } from 'store';
import { Status } from 'enums/status';

const initialState: Status = Status.Loading;

export const statusSlice = createSlice({
  name: 'status',
  initialState,
  reducers: {
    setStatus: (state, action: PayloadAction<any>) => action.payload,
    resetStatus: () => initialState,
  },
});

export const { setStatus, resetStatus } = statusSlice.actions;

export const selectStatus = (state: RootState) => state.status;

export default statusSlice;
