import React, { useState } from "react";
import React from "react";
import Select from "react-select";


const RecommendationSelect = ({options}) => {
    const [selectedValues, setSelectedValues] = useState([]);
    return (
      <Select
        options={options}
        isMulti
        menuPlacement="auto"
        menuPortalTarget={document.body}
        styles={{
          control: (baseStyles, state) => ({
            ...baseStyles,
            maxHeight: "40px",
            overflowY: "auto",
          }),
          menu: (provided) => ({
            ...provided,
            maxHeight: "150px",
            overflowY: "auto",
          }),
        }}
        value={selectedValues}
        onChange={(values) => setSelectedValues(values)}
      />
    );
}


const ItemSelect = ({options}) => {
    const [selectedValues, setSelectedValues] = useState([]);
    return (
      <Select
        options={options}
        isMulti
        menuPlacement="auto"
        menuPortalTarget={document.body}
        styles={{
          control: (baseStyles, state) => ({
            ...baseStyles,
            maxHeight: "40px",
            overflowY: "auto",
          }),
          menu: (provided) => ({
            ...provided,
            maxHeight: "150px",
            overflowY: "auto",
          }),
        }}
        value={selectedValues}
        onChange={(values) => setSelectedValues(values)}
      />
    );
  };

export {RecommendationSelect, ItemSelect};