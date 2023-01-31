import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { RootState } from 'store';

const initialState = {
  jobs_in_queue: 0,
  max_queue_size: 0,
  queue_position: 0,
};

export const queueSlice = createSlice({
  name: 'queue',
  initialState,
  reducers: {
    setQueue: (state, action: PayloadAction<any>) => ({
      ...state,
      ...action.payload,
    }),
    resetQueue: () => initialState,
  },
});

export const { setQueue, resetQueue } = queueSlice.actions;

export const selectJobsInQueue = (state: RootState) => state.queue.jobs_in_queue;
export const selectQueuePosition = (state: RootState) => state.queue.queue_position;

export default queueSlice;
