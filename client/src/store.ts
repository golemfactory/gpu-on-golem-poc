import { configureStore } from '@reduxjs/toolkit';
import { createWrapper } from 'next-redux-wrapper';
import dataSlice from 'slices/data';
import errorSlice from 'slices/error';
import nodesSlice from 'slices/nodes';
import queueSlice from 'slices/queue';
import statusSlice from 'slices/status';

export const store = () =>
  configureStore({
    reducer: {
      [dataSlice.name]: dataSlice.reducer,
      [errorSlice.name]: errorSlice.reducer,
      [nodesSlice.name]: nodesSlice.reducer,
      [queueSlice.name]: queueSlice.reducer,
      [statusSlice.name]: statusSlice.reducer,
    },
  });

export type AppStore = ReturnType<typeof store>;
export type RootState = ReturnType<AppStore['getState']>;

export default createWrapper<AppStore>(store);
