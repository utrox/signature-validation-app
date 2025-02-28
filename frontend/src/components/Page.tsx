import React from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import PageTitle from "./Routing/PageTitle";

interface PageProps {
  children: React.ReactNode;
  addNavbar?: boolean;
  addFooter?: boolean;
  title?: string;
}

const Page: React.FC<PageProps> = ({
  children,
  addNavbar = true,
  addFooter = true,
  title = "",
}) => {
  console.log(addNavbar, addFooter, title);
  return (
    <>
      <PageTitle title={title} />
      {addNavbar && <Navbar />}
      {children}
      {addFooter && <Footer />}
    </>
  );
};

export default Page;
