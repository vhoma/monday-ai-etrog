"use client";
import { useCallback, useState, useMemo } from "react";
import styles from "./page.module.css";
import { AppContextProvider } from "@/components/context-provider/app-context-provider";
import BasePromptLayout from "@/examples/basic-prompt-layout/prompt-layout";
import { Button } from "monday-ui-react-core";

export default function Home() {
  const [displayedApp, setAppToDisplay] = useState("");

  const renderApp = useMemo(() => {
    switch (displayedApp) {
      case "BasePromptLayout":
        return <BasePromptLayout />;
      default:
        return (
          <div>
            <Button onClick={() => renderExampleApp("BasePromptLayout")}>
              Call The Team
            </Button>
          </div>
        );
    }
  }, [displayedApp]);
  const renderExampleApp = (type = "ContextExplorerExample") => {
    setAppToDisplay(type);
  };
  return (
    <div className={styles.App}>
      <AppContextProvider>
        <>{renderApp}</>
      </AppContextProvider>
    </div>
  );
}
