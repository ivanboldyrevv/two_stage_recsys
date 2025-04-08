import React from "react";
import { useState, useEffect } from "react";

import "./App.css";

import ItemCard from "./components/ItemCard";
import ItemsContainer from "./components/ItemsContainer";
import ReactPaginate from "react-paginate";
import Select from "react-select";
import {Toaster, toast} from "sonner";

import usePages from "./api/pages";
import useCustomer from "./api/customer";
import useRecs from "./api/recs";
import { fetchGroups } from "./api/filter";
import { insertTransaction } from "./api/transaction";


const App = () => {
  const randomSeed = undefined;
  const [customerData, setCustomer] = useState([]);

  const pageSize = 15;
  const [currentPage, setCurrentPage] = useState(15);
  const [totalPages, setTotalPages] = useState(0);  
  const [pageContent, setPageContent] = useState([]);

  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(undefined);

  const [recsContent, setRecsContent] = useState([]);

  const handleTransactionClick = (articleUUID) => {
    insertTransaction(customerData.customer_uuid, articleUUID);
    useRecs(customerData.customer_uuid, setRecsContent);
    toast.success('Success!', {
      description: 'Transaction was saved successfully',
      duration: 4000,
      position: 'top-right',
      icon: '🫡',
      style: {
        background: '#fff',
        color: '#000',
        border: '1px solid #4ade80'
      },
    });
  }

  const handlePageClick = (event) => {
    setCurrentPage(event.selected);
  };

  useEffect(() => {
    fetchGroups(setGroups);
    useCustomer(setCustomer, randomSeed);
  }, [])

  useEffect(() => {
    if (customerData.customer_uuid) {    
      useRecs(customerData.customer_uuid, setRecsContent);
    }
  }, [customerData.customer_uuid]);
  
  useEffect(() => {
    usePages(setPageContent, setTotalPages, currentPage, pageSize, undefined, selectedGroup);
  }, [selectedGroup, currentPage])

  const items = pageContent.map((article) => (
    <ItemCard 
      key={article.article_uuid}
      uuid={article.article_uuid}
      imgUrl={article.imageUrl} 
      itemCategory={article.product_group_name} 
      itemName={article.prod_name}
      handleClick={handleTransactionClick}
    />
  ));

  const recs = recsContent.map((article) => (
    <ItemCard 
      key={article.article_uuid}
      uuid={article.article_uuid}
      imgUrl={article.imageUrl} 
      itemCategory={article.product_group_name} 
      itemName={article.prod_name}
    />
  ))


  return (
    <div className="content">
      <Toaster
        position="top-right"
        expand={false}
        richColors={true}
        visibleToasts={3}
      />
      <div className="settings">
        <div className="navigation-container">
          <p>Navigation</p>
          <hr></hr>
          <button>Main</button>
          <button>Example</button>
          <button>Customer transaction</button>
          <button>Settings</button>
        </div>
        <div className="filter-container">
          <p>Articles filter`s</p>
          <hr></hr>
          <Select
            classNamePrefix={"filter-select"}
            options={groups}
            value={selectedGroup}
            placeholder={"Select article group..."}
            onChange={(values) => setSelectedGroup(values)}
          />
        </div>
      </div>

      <div className="items-grid">
        <div className="items-container">
          <ItemsContainer
            items={items}
          />
        </div>
        <div className="pagination-grid">
        <ReactPaginate
            containerClassName="custom-pagination"
            pageLinkClassName="custom-page-link"
            activeLinkClassName="active-link"
            previousLabel={""}
            nextLabel={""}
            activePage={currentPage}
            onPageChange={handlePageClick}
            pageRangeDisplayed={3}
            pageCount={totalPages}
            renderOnZeroPageCount={null}
        />
        </div>
        <div className="recs-container">
          <hr></hr>
          <p>Recommendation`s</p>
          <ItemsContainer
            items={recs}
          />
        </div>
      </div>
    </div>
  );
};

export default App;
