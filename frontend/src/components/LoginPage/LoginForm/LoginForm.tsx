/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from "react";
import {
  Form,
  TextInput,
  Button,
  ToastNotification,
} from "carbon-components-react";
import { InlineLoading, PasswordInput, Tooltip } from "@carbon/react";
import { CheckboxGroup, Checkbox } from "@carbon/react";
import styles from "src/components/LoginPage/LoginForm/LoginForm.module.scss";
import botLogoSrc from "src/assets/Querius_Logo.png";
import en from "src/locals/en.json";
import { login } from "src/services/loginService";
import { useNavigate } from "react-router-dom";
import { encryptValue } from "src/services/encryptionService";
import { Information } from "@carbon/icons-react";

const LoginForm: React.FC = () => {
  const [errorNotification, setErrorNotification] = React.useState("");
  const [warnNotification, setWarnNotification] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(false);
  const [loginFormData, setLoginFormData] = React.useState({
    tenantID: "",
    apiKey: "",
    userID: "",
  });
  const [invalidFields, setInvalidFields] = React.useState({
    apiKey: false,
    userID: false,
    tenantID: false,
  });
  const [saveCredentials, setSaveCredentials] = React.useState(false);
  const [isSignInEnabled, setIsSignInEnabled] = React.useState(false);
  const navigate = useNavigate();

  const learnHowLink = `https://www.ibm.com/docs/en/storage-insights?topic=configuring-user-access-management`;

  const handleFormInputChange = (event: any) => {
    const { name, value } = event.target;
    setLoginFormData((prevData) => {
      const newFormData = {
        ...prevData,
        [name]: value,
      };
      setIsSignInEnabled(
        newFormData?.userID.trim() !== "" &&
          newFormData?.tenantID.trim() !== "" &&
          newFormData?.apiKey.trim() !== ""
      );
      return newFormData;
    });
    setInvalidFields((prevFields) => ({
      ...prevFields,
      [name]: false,
    }));
  };

  const handleBlur = (fieldName: string) => {
    if (fieldName === "apiKey") {
      setInvalidFields({
        ...invalidFields,
        apiKey: loginFormData?.apiKey.trim() === "",
      });
    } else if (fieldName === "userID") {
      setInvalidFields({
        ...invalidFields,
        userID: loginFormData?.userID.trim() === "",
      });
    } else if (fieldName === "tenantID") {
      setInvalidFields({
        ...invalidFields,
        tenantID: loginFormData?.tenantID.trim() === "",
      });
    }
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();
    setIsLoading(true);
    const apiKey = encryptValue(loginFormData.apiKey)
    const payload = {
      username: loginFormData?.userID,
      api_key: apiKey,
      tenant_id: loginFormData?.tenantID,
    };

    const response = await login(payload);
    setIsLoading(false);

    if (response?.user_data) {
      const authCredentials = {
        userID: response.user_data.username,
        xApiKey: loginFormData?.apiKey,
        tenantID: response.user_data.tenant_id,
      };

      localStorage.setItem(
        "authCredentials",
        btoa(JSON.stringify(authCredentials))
      ); // Encode as base64

      if (saveCredentials) {
        localStorage.setItem(
          "rememberedCredentials",
          btoa(JSON.stringify(authCredentials))
        );
        localStorage.setItem("saveCredentials", "true");
      } else {
        localStorage.removeItem("rememberedCredentials");
        localStorage.removeItem("saveCredentials");
      }

      navigate("/chat-dashboard");
    } else {
      const errorMessage =
        response?.response?.data?.detail?.message ||
        "Failed to login. Please try again";
      if (errorMessage) {
        setErrorNotification(errorMessage);
      }
    }
  };

  React.useEffect(() => {
    const rememberedCredentials = localStorage.getItem("rememberedCredentials");
    const savedRememberMe = localStorage.getItem("saveCredentials") === "true";

    if (rememberedCredentials && savedRememberMe) {
      try {
        const credentials = JSON.parse(atob(rememberedCredentials)); // Decode and parse base64-encoded credentials
        const newFormData = {
          ...loginFormData,
          userID: credentials.userID,
          apiKey: credentials.xApiKey,
          tenantID: credentials.tenantID,
        };
        setIsSignInEnabled(
          newFormData?.userID.trim() !== "" &&
            newFormData?.apiKey.trim() !== "" &&
            newFormData?.tenantID.trim() !== ""
        );
        setSaveCredentials(savedRememberMe);
        setLoginFormData(newFormData);
      } catch (error) {
        console.error(en.failedToParseCredentials, error);
      }
    }
  }, []);

  return (
    <div>
      <div className={styles.loginNotification}>
        {warnNotification && (
          <ToastNotification
            kind="warning"
            title="Access Denied!"
            subtitle={warnNotification}
            onCloseButtonClick={() => setWarnNotification("")}
          />
        )}
        {errorNotification && (
          <ToastNotification
            kind="error"
            title="Error"
            subtitle={errorNotification}
            onCloseButtonClick={() => setErrorNotification("")}
          />
        )}
      </div>
      <div className={styles.loginCard}>
        <div>
          <div className={styles.loginContainer}>
            <div className={styles.loginDesc}>
              <img src={botLogoSrc} alt="Logo" className={styles.queriusLogo} />
              <div className={styles.loginFormInfo}>
                <h2 className={styles.loginTitle}>{en.signInAccount}</h2>
                <p className={styles.loginDescription}>{en.logInMessage}</p>
              </div>
            </div>
            <Form
              id="loginFormContainer"
              onSubmit={handleSubmit}
              className={styles.loginFormContent}
            >
              <div>
                <TextInput
                  className={styles.loginFormInputField}
                  id="userID"
                  name="userID"
                  type="text"
                  labelText={en.userID}
                  value={loginFormData.userID}
                  onChange={handleFormInputChange}
                  onBlur={() => handleBlur("userID")}
                  required
                  invalid={invalidFields.userID}
                  invalidText={
                    invalidFields.userID ? en.requiredFieldLoginEmail : ""
                  }
                />
              </div>

              <div>
                <TextInput
                  className={styles.loginFormInputField}
                  id="tenantID"
                  name="tenantID"
                  type="text"
                  labelText={en.tenantId}
                  value={loginFormData.tenantID}
                  onChange={handleFormInputChange}
                  onBlur={() => handleBlur("tenantID")}
                  required
                  invalid={invalidFields.tenantID}
                  invalidText={
                    invalidFields.tenantID ? en.requiredFieldTenantID : ""
                  }
                />
              </div>
              <div className={styles.apiKeyField}>
                <span className={styles.infoIcon}>
                  <Tooltip
                    align="right"
                    label={
                      <div className={styles.tooltipContent}>
                          <a
                            href={learnHowLink}
                            target="_blank"
                            rel="noreferrer"
                          >
                            {en.generatingAPIKey}
                          </a>
                      </div>
                    }
                  >
                    <Information />
                  </Tooltip>
                </span>
                <PasswordInput
                  className={styles.loginFormIApiKeyField}
                  id="apiKey"
                  name="apiKey"
                  type={"password"}
                  labelText={en.apiKey}
                  value={loginFormData.apiKey}
                  onChange={handleFormInputChange}
                  onBlur={() => handleBlur("apiKey")}
                  required
                  invalid={invalidFields.apiKey}
                  invalidText={
                    invalidFields.apiKey ? en.requiredFieldApiKey : ""
                  }
                />
              </div>

              <div>
                <CheckboxGroup>
                  <Checkbox
                    disabled={!isSignInEnabled}
                    labelText={en.saveCredentials}
                    id="checkbox-label-1"
                    checked={saveCredentials}
                    onChange={(_: any, { checked }: any) =>
                      setSaveCredentials(checked)
                    }
                  />
                </CheckboxGroup>
              </div>

              <div className={styles.loginFormActions}>
                <Button
                  className={styles.signUpButton}
                  type="submit"
                  disabled={!isSignInEnabled}
                >
                  {!isLoading && <div>{en.signIn}</div>}
                  {isLoading && (
                    <div className={styles.loader}>
                      <InlineLoading
                        status="active"
                        iconDescription={en.loading}
                        description={en.inlineLoadingDescription}
                        className={styles.ackInlineLoading}
                      />
                    </div>
                  )}
                </Button>
              </div>
            </Form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
