import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { RootState } from 'store';

const initialState: Data = {
  eta: undefined,
  img_url: undefined,
  intermediary_images: undefined,
  progress: undefined,
  provider: undefined,
};

export const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {
    setData: (state, action: PayloadAction<Data>) => ({ ...state, ...action.payload }),
    resetData: () => initialState,
  },
});

export const { setData, resetData } = dataSlice.actions;

export const selectData = (state: RootState) => state.data;

export default dataSlice;
