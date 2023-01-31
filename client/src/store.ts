import { configureStore } from '@reduxjs/toolkit';
import { createWrapper } from 'next-redux-wrapper';
import nodesSlice from 'slices/nodes';
import queueSlice from 'slices/queue';
import statusSlice from 'slices/status';

export const store = () =>
  configureStore({
    reducer: {
      [nodesSlice.name]: nodesSlice.reducer,
      [queueSlice.name]: queueSlice.reducer,
      [statusSlice.name]: statusSlice.reducer,
    },
  });

export type AppStore = ReturnType<typeof store>;
export type RootState = ReturnType<AppStore['getState']>;

export default createWrapper<AppStore>(store);
