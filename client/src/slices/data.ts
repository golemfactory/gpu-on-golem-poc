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
  socketUrl: null,
};

export const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {
    setData: (state, action: PayloadAction<Partial<Data>>) => ({ ...state, ...action.payload }),
    setEta: (state, action: PayloadAction<number>) => ({ ...state, eta: action.payload }),
    setJobId: (state, action: PayloadAction<string>) => ({ ...state, job_id: action.payload }),
    setProvider: (state, action: PayloadAction<string>) => ({ ...state, provider: action.payload }),
    setSocketUrl: (state, action: PayloadAction<string>) => ({ ...state, socketUrl: action.payload }),
    resetData: () => initialState,
  },
});

export const { setData, setEta, setJobId, setProvider, setSocketUrl, resetData } = dataSlice.actions;

export const selectData = (state: RootState) => state.data;
export const selectEta = (state: RootState) => state.data.eta;
export const selectJobId = (state: RootState) => state.data.job_id;
export const selectSocketUrl = (state: RootState) => state.data.socketUrl;

export default dataSlice;
