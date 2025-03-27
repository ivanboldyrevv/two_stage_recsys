import React, { useState } from 'react';
import ReactPaginate from 'react-paginate';

const Paginate = () => {
    const [currentPage, setCurrentPage] = useState(0);

    const handlePageClick = (event) => {
        setCurrentPage(event.selected);
        console.log(`Selected page: ${event.selected + 1}`);
    };

    return (
        <ReactPaginate
            containerClassName="custom-pagination"
            pageLinkClassName="custom-page-link"
            activeLinkClassName="active-link"
            activePage={currentPage}
            onPageChange={handlePageClick}
            pageRangeDisplayed={5}
            pageCount={5}
            renderOnZeroPageCount={null}
        />
    );
};

export default Paginate;