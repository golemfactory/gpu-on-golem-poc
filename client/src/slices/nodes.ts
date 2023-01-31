import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { RootState } from 'store';

const initialState: NodeInstance[] = [];

export const nodesSlice = createSlice({
  name: 'nodes',
  initialState,
  reducers: {
    setNodes: (state, action: PayloadAction<NodeInstance[]>) => action.payload,
    resetNodes: () => initialState,
  },
});

export const { setNodes, resetNodes } = nodesSlice.actions;

export const selectNodes = (state: RootState) => state.nodes;

export default nodesSlice;
