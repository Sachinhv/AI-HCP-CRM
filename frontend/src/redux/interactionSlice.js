import { createSlice } from "@reduxjs/toolkit";

const initialState = {

    hcp_name:"",

    interaction_type:"",

    date:"",

    time:"",

    attendees:"",

    topics_discussed:"",

    materials_shared:"",

    samples_distributed:"",

    sentiment:"",

    outcomes:"",

    follow_up:""

};

const interactionSlice=createSlice({

    name:"interaction",

    initialState,

    reducers:{

        updateInteraction:(state,action)=>{

            return {

                ...state,

                ...action.payload

            };

        }

    }

});

export const {updateInteraction}=interactionSlice.actions;

export default interactionSlice.reducer;