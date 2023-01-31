import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { RootState } from 'store';

const initialState: Data = {
  eta: undefined,
  img_url: undefined,
  intermediary_images: undefined,
  job_id: undefined,
  progress: undefined,
  provider: undefined,
};

export const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {
    setData: (state, action: PayloadAction<Data>) => ({ ...state, ...action.payload }),
    setJobId: (state, action: PayloadAction<string>) => ({ ...state, job_id: action.payload }),
    resetData: () => initialState,
  },
});

export const { setData, setJobId, resetData } = dataSlice.actions;

export const selectData = (state: RootState) => state.data;
export const selectJobId = (state: RootState) => state.data.job_id;

export default dataSlice;
