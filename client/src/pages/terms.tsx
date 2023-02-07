import { ReactNode, useState } from 'react';
import { Layout } from 'components';
import { renderIcon } from 'assets/utils';

function Terms() {
  const [state, setState] = useState('terms');

  const handleClick = (state: string) => {
    window?.scroll({ top: 0, behavior: 'smooth' });
    setState(state);
  };

  const handleReset = () => handleClick('terms');

  return (
    <Layout footer={false}>
      <div className="mt-[20rem] mb-[8rem] font-light lg:mt-[15rem]">
        {state === 'terms' && (
          <>
            <h1 className="text-18">Golem Image Generator</h1>
            <h2 className="mb-[2.6rem] text-18">Terms of Use</h2>
            <h2 className="mb-[0.6rem] text-left text-[1.4rem] font-bold">Important information</h2>
            <p className="text-justify font-sans text-[1.4rem]">
              Prior to obtaining access to the Golem Image Generator (as defined below), please read the following
              information carefully and ensure that you understand each provision. These Terms comprise an agreement
              between the end-user (“{bold('You')}” or “{bold('User')}”) and Golem. By using this Golem Image Generator,
              including our application programming interface, software, tools, developer services, data, documentation,
              and website related to Golem Image Generator (hereinafter collectively as “{bold('Services')}”) you
              confirm that you have read, understood, and you accept all of the terms and conditions contained in this
              Terms. These Terms of apply to every territory where Golem Image Generator is available and include our
              Content Policy and Privacy Policy and other documentation, guidelines, or policies we may to You.
            </p>
            <p className="my-[1rem] text-justify font-sans text-[1.4rem]">
              {underline(
                'IF YOU DO NOT AGREE TO THE TERMS OF USE OF THIS GOLEM IMAGE GENERATOR OR YOU ARE UNABLE TO COMPLY WITH THESE TERMS, YOU MUST DISCONTINUE THE USING OF THE GOLEM IMAGE GENERATOR NOW. IN THIS CASE DISCONTINUING THE USE TERMINATE THE AGREEMENT BETWEEN YOU AND GOLEM. FAILURE TO COMPLY WITH THIS DIRECTIVE MAY RESULT IN A VIOLATION OF THE APPLICABLE LAWS OR REGULATIONS.',
              )}
            </p>
            <br />
            <ol className="text-justify">
              {renderList('Preliminary provisions', [
                <>
                  {underline('We and You.')} In these Terms “Golem”, "we" and "us" refers to{' '}
                  {bold('Golem Factory GmbH')}, a company organized and existing under the laws of Switzerland, with its
                  registered office in Zug at Dammstrasse 16 (street), Postal code: 6300 Zug, entered into the
                  commercial register under CHE-143.168.192 number (“{bold('Golem')}”) and we offer the multimodal
                  generative model that can create realistic images and art from a description in natural language (“
                  {bold('Golem Image Generator')}”). These terms of use ("
                  {bold('Terms')}”) apply to the rights and obligations of You using the Golem Image Generator.`
                </>,
                <>
                  {underline('Availability.')} Availability of the Services for the User residing outside the territory
                  of the Switzerland may be limited in whole or in part.
                </>,
                <>
                  {underline('OpenRAIL license.')} Multimodal generative model being used in this Golem Image Generator
                  is copyrighted to Robin Rombach and Patrick Esser and contributors under{' '}
                  {bold('CreativeML Open RAIL-M license')} dated August 22, 2022, a copy of which is attached to these
                  Terms in Attachment A.
                </>,
                <>
                  {underline('Additional terms.')} If a given service offered by Golem requires separate regulation, or
                  if it results from its specificity (e.g. promotions or trading competition), its terms and conditions
                  may be specified in additional terms, other than these Terms, which will constitute an integral part
                  of these Terms.
                </>,
              ])}
              {renderList('Access', [
                <>
                  {underline('Age limit.')} You must be 18 years or older and able to form a legally binding agreement
                  online to use the Services, and have the full, right, power and authority to enter into and to comply
                  with the obligations under these Terms. If you use the Services on behalf of another person or entity,
                  you must have the authority to accept the Terms on their behalf. By using the Services you declare
                  that you meet the required age criteria.
                </>,
              ])}
              {renderList('Usage requirements', [
                <>
                  {underline('Use of Services.')} You may access, and we grant you a non-exclusive, no-charge,
                  royalty-free right to use, the Services in accordance with these Terms. You will comply with these
                  Terms and all applicable laws when using the Services. We and our affiliates own all rights, title,
                  and interest in and to the Services.
                </>,
                <>
                  {underline('Feedback.')} We appreciate feedback, comments, ideas, proposals and suggestions for
                  improvements. If you provide any of these things, we may use it without restriction or compensation to
                  you.
                </>,
                <>
                  {underline('Restrictions.')} You may not (i) use the Services in a way that infringes, misappropriates
                  or violates any person’s rights; (ii) reverse assemble, reverse compile, decompile, translate or
                  otherwise attempt to discover the source code or underlying components of models, algorithms, and
                  systems of the Services (except to the extent such restrictions are contrary to applicable law); (iii)
                  use any method to extract data from the Services, including web scraping, web harvesting, or web data
                  extraction methods, other than as permitted through the API; (iv) represent that output from the
                  Services was human-generated when it is not; or (v) buy, sell, or transfer API keys without our prior
                  consent. You will comply with any rate limits and other requirements in our documentation. You may use
                  Services only in geographies currently supported by Golem.
                </>,
                <>
                  {underline('Third Party Services.')} Any third party software, services, or other products you use in
                  connection with the Services are subject to their own terms, and we are not responsible for third
                  party products.
                </>,
              ])}
              {renderList('Content', [
                <>
                  {underline('Your Content.')} You may provide input to the Services (“{bold('Input')}”), and receive
                  output generated and returned by the Services based on the Input (“{bold('Output')}”). Input and
                  Output are collectively “{bold('Content')}.” As between the parties and to the extent permitted by
                  applicable law, you own all Input, and subject to your compliance with these Terms, Golem hereby
                  assigns to you all its right, title and interest in and to Output. Golem may use Content as necessary
                  to provide and maintain the Services, comply with applicable law, and enforce our policies.
                </>,
                <>
                  {underline('Content accountability.')} You are responsible for the Input and for the Output you
                  generate and its subsequent uses, including for ensuring that it does not violate any applicable law
                  or these Terms.
                </>,
                <>
                  {underline('Similarity of Content.')} Due to the nature of machine learning, Output may not be unique
                  across users and the Golem Image Generator may generate the same or similar output for Golem or a
                  third party. For example, you may provide input to a model such as “Color is the sun” and receive
                  output such as the “picture of the sun”. Other users may also ask similar questions and receive the
                  same response. Responses that are requested by and generated for other users are not considered your
                  Content.
                </>,
                <>
                  {underline('Content Policy.')} You must comply with the Golem content policy and use based
                  restrictions set forth in Attachment B.
                </>,
                <>
                  {underline('Content review.')} Golem may use third party contractors to review Content for safety and
                  moderation purposes, which however, shall not be deemed as the Golem’s guarantee or obligations to
                  verify the Content to confirm its compliance with these Terms.
                </>,
                <>
                  {underline('Copyright Complaints.')} If you believe that your intellectual property rights have been
                  infringed, please send notice to the address below. We may delete or disable content alleged to be
                  infringing and may terminate accounts of repeat infringers:
                  <br />
                  <div className="my-[1rem] text-center italic">
                    {bold('Golem Factory GmbH')}, Dammstrasse 16 (street), Postal code: 6300 Zug
                  </div>
                </>,
                <>
                  {underline('Claims.')} Written claims concerning copyright infringement must include the following
                  information:
                  <ol>
                    <li>
                      A physical or electronic signature of the person authorized to act on behalf of the owner of the
                      copyright interest;
                    </li>
                    <li>A description of the copyrighted work that you claim has been infringed upon;</li>
                    <li>A description of where the material that you claim is infringing is located on the site;</li>
                    <li>Your address, telephone number, and e-mail address;</li>
                    <li>
                      A statement by you that you have a good-faith belief that the disputed use is not authorized by
                      the copyright owner, its agent, or the law; and
                    </li>
                    <li>
                      A statement by you, made under penalty of perjury, that the above information in your notice is
                      accurate and that you are the copyright owner or authorized to act on the copyright owner’s
                      behalf.
                    </li>
                  </ol>
                </>,
              ])}
              {renderList('Our Liability', [
                <>
                  {underline('Indemnity.')} You will defend, indemnify, and hold harmless us, our affiliates, and our
                  personnel, from and against any claims, losses, and expenses (including attorneys’ fees) arising from
                  or relating to your use of the Services, including your Content, products or services you develop or
                  offer in connection with the Services, and your breach of these Terms or violation of applicable law.
                </>,
                <>
                  {underline('Disclaimer.')} Golem Image Generator and Services are continuously developed during the
                  prototyping stage, thus features that Golem offers are still on an alpha, preview, early access, or
                  beta basis and therefore Golem Image Generator and Services are provided “AS IS.” Except to the extent
                  prohibited by law, we and our affiliates and licensors make no warranties (express, implied, statutory
                  or otherwise) with respect to the Services, and disclaim all warranties including but not limited to
                  warranties of merchantability, fitness for a particular purpose, satisfactory quality,
                  non-infringement, and quiet enjoyment, and any warranties arising out of any course of dealing or
                  trade usage. We do not warrant that the Services will be uninterrupted, accurate or error free, or
                  that any content will be secure or not lost or altered.
                </>,
                <>
                  {underline('Limitations of Liability.')} Neither we nor any of our affiliates or licensors will be
                  liable for any indirect, incidental, special, consequential or exemplary damages, including damages
                  for loss of profits, goodwill, use, or data or other losses, even if we have been advised of the
                  possibility of such damages.
                </>,
              ])}
              {renderList('Confidentiality, Security and Data Protection', [
                <>
                  {underline('Confidentiality.')} You may be given access to Confidential Information of Golem, its
                  affiliates and other third parties. You may use Confidential Information only as needed to use the
                  Services as permitted under these Terms. You may not disclose Confidential Information to any third
                  party, and you will protect Confidential Information in the same manner that you protect your own
                  confidential information of a similar nature, using at least reasonable care. Confidential Information
                  means nonpublic information that Golem or its affiliates or third parties designate as confidential or
                  should reasonably be considered confidential under the circumstances, including software,
                  specifications, and other nonpublic business information. Confidential Information does not include
                  information that: (i) is or becomes generally available to the public through no fault of yours; (ii)
                  you already possess without any confidentiality obligations when you received it under these Terms;
                  (iii) is rightfully disclosed to you by a third party without any confidentiality obligations; or (iv)
                  you independently developed without using Confidential Information. You may disclose Confidential
                  Information when required by law or the valid order of a court or other governmental authority if you
                  give reasonable prior written notice to Golem and use reasonable efforts to limit the scope of
                  disclosure, including assisting us with challenging the disclosure requirement, in each case where
                  possible.
                </>,
                <>
                  {underline('Security.')} You must implement reasonable and appropriate measures designed to help
                  secure your access to and use of the Services. If you discover any vulnerabilities or breaches related
                  to your use of the Services, you must promptly contact Golem and provide details of the vulnerability
                  or breach.
                </>,
              ])}
              {renderList('General Terms and Updates', [
                <>
                  {underline('Use of Brands.')} You may not use Golem’s or any of its affiliates’ names, logos, or
                  trademarks, without our prior written consent.
                </>,
                <>
                  {underline('Current version.')} The current Terms are available at{' '}
                  {link('https://gpu.dev-test.golem.network/')}.
                </>,
                <>
                  {underline('Updates.')} The Terms may be regularly reviewed and updated as required. Each document
                  comprising the Terms will include information on when it was last reviewed. You are advised to check
                  these Terms periodically to familiarize yourself with any changes to the Terms. Please observe what
                  version of the Terms applies to you before you use Golem Image Generator.
                </>,
                <>
                  {underline('Changes approval.')} Golem, in its sole discretion, reserves the right to make changes to
                  the Terms or to issue new Terms in the course of the agreement with the User, in particular due to
                  changes in the applicable law or due to changes in the functionality of the Services in order to
                  provide its Users with more convenient terms of using both the Golem Image Generator and Services or
                  in case of occurrence of other important reasons, including reasons of technological nature of the
                  Golem Image Generator functioning. Changes are binding on users of the Services and will take effect
                  immediately upon posting. As a User, You agree to be bound by any changes, variations, or
                  modifications to our Terms and your continued use of the Golem Image Generator shall constitute
                  acceptance of any such changes, variations, or modifications.
                </>,
                <>
                  Unless a representation, which may be subject to change without notice from time to time, is expressed
                  to be given at a specific date, each representation is deemed to be repeated by you each time you use
                  the Services. When a representation is repeated, it is applied to the circumstances existing at the
                  time of repetition. You accept that Golem does not hold an obligation to verify your status with
                  respect to your representations or obligations under the Terms.
                </>,
                <>
                  {underline('Assignment and Delegation.')} You may not assign or delegate any rights or obligations
                  under these Terms, including in connection with a change of control. Any purported assignment and
                  delegation shall be null and void. We may assign these Terms in connection with a merger, acquisition
                  or sale of all or substantially all of our assets, or to any affiliate or as part of a corporate
                  reorganization.
                </>,
              ])}
              {renderList('Jurisdiction and Governing Law', [
                <>
                  {underline('Choice of Law.')} This Terms and all related documents and all matters arising out of or
                  relating to these Terms, whether sounding in contract, tort, or statute are governed by, and construed
                  in accordance with, the laws of Switzerland without giving effect to the Swiss conflict of law
                  provisions. The application of the United Nations Convention for Contracts for the International Sales
                  of Goods is hereby expressly excluded.
                </>,
                <>
                  {underline('Court.')} You hereto irrevocably agrees that any legal action or proceeding with respect
                  to these Terms and the rights and obligations arising hereunder, or for recognition and enforcement of
                  any judgment in respect of these Terms and the rights and obligations arising hereunder brought by You
                  hereto or yours successors or assigns, shall be brought and determined exclusively in the courts of
                  Zürich, Switzerland, venue being Zurich 1. You hereby irrevocably submits to the exclusive
                  jurisdiction of these courts and waive the defense of inconvenient forum to the maintenance of any
                  action or proceeding in such venue.
                </>,
              ])}
              {renderList('Contacting Us', [
                <>
                  {underline('E-mail.')} Should you have any question about these Terms, or wish to contact us for any
                  reason whatsoever, please do so by sending us an email at office@golem.network.
                </>,
              ])}
            </ol>
            <div className="mt-[5rem] flex flex-col justify-between text-left font-sans text-[1.4rem] md:flex-row">
              <div>
                <p onClick={() => handleClick('attachment-a')}>
                  <span className="cursor-pointer text-blue">Attachment A</span> - CreativeML Open RAIL-M
                </p>
                <p onClick={() => handleClick('attachment-b')}>
                  <span className="cursor-pointer text-blue">Attachment B</span> - Content Policy
                </p>
              </div>
              <div className="mt-[1.2rem] md:mt-0">
                <p>Date: 30.01.2023</p>
                <p>Version: 1.0.</p>
              </div>
            </div>
          </>
        )}
        {state === 'attachment-a' && (
          <>
            <div className="flex">
              <div
                className="mr-[1rem] h-[2.1rem] w-[2.1rem] cursor-pointer bg-contain bg-no-repeat"
                style={{ backgroundImage: `url(${renderIcon('back')})` }}
                onClick={handleReset}
              />
              <h2 className="mb-[0.6rem] text-left text-[1.4rem]">
                {bold('Attachment A')} - Golem Image Generator - Terms of Use
              </h2>
            </div>
            <h2 className="mt-[2.6rem] text-18">CreativeML Open RAIL-M</h2>
            <h2 className="text-18">Source: {link('https://stablediffusionweb.com/license')}</h2>
            <div className="my-[2.6rem] h-[0.1rem] w-full bg-stone " />
            <div className="text-left text-12 font-light">
              <p className="mb-[1.6rem]">Copyright (c) 2022 Robin Rombach and Patrick Esser and contributors</p>
              <p>CreativeML Open RAIL-M</p>
              <p className="mb-[1.6rem]">dated August 22, 2022</p>
              <h3 className="my-[1.6rem]">Section I: PREAMBLE</h3>
              <p className="mb-[1.6rem]">
                Multimodal generative models are being widely adopted and used, and have the potential to transform the
                way artists, among other individuals, conceive and benefit from AI or ML technologies as a tool for
                content creation.
              </p>
              <p className="mb-[1.6rem]">
                Notwithstanding the current and potential benefits that these artifacts can bring to society at large,
                there are also concerns about potential misuses of them, either due to their technical limitations or
                ethical considerations.
              </p>
              <p className="mb-[1.6rem]">
                In short, this license strives for both the open and responsible downstream use of the accompanying
                model. When it comes to the open character, we took inspiration from open source permissive licenses
                regarding the grant of IP rights. Referring to the downstream responsible use, we added use-based
                restrictions not permitting the use of the Model in very specific scenarios, in order for the licensor
                to be able to enforce the license in case potential misuses of the Model may occur. At the same time, we
                strive to promote open and responsible research on generative models for art and content generation.
              </p>
              <p className="mb-[1.6rem]">
                Even though downstream derivative versions of the model could be released under different licensing
                terms, the latter will always have to include - at minimum - the same use-based restrictions as the ones
                in the original license (this license). We believe in the intersection between open and responsible AI
                development; thus, this License aims to strike a balance between both in order to enable responsible
                open-science in the field of AI.
              </p>
              <p className="mb-[1.6rem]">
                This License governs the use of the model (and its derivatives) and is informed by the model card
                associated with the model.
              </p>
              <p className="mb-[1.6rem]">NOW THEREFORE, You and Licensor agree as follows:</p>
              <ol className="font-mono text-12 font-light">
                {renderList('Definitions')}
                <ul>
                  <li>
                    "License" means the terms and conditions for use, reproduction, and Distribution as defined in this
                    document.
                  </li>
                  <li>
                    "Data" means a collection of information and/or content extracted from the dataset used with the
                    Model, including to train, pretrain, or otherwise evaluate the Model. The Data is not licensed under
                    this License.
                  </li>
                  <li>
                    "Output" means the results of operating a Model as embodied in informational content resulting
                    therefrom.
                  </li>
                  <li>
                    "Model" means any accompanying machine-learning based assemblies (including checkpoints), consisting
                    of learnt weights, parameters (including optimizer states), corresponding to the model architecture
                    as embodied in the Complementary Material, that have been trained or tuned, in whole or in part on
                    the Data, using the Complementary Material.
                  </li>
                  <li>
                    "Derivatives of the Model" means all modifications to the Model, works based on the Model, or any
                    other model which is created or initialized by transfer of patterns of the weights, parameters,
                    activations or output of the Model, to the other model, in order to cause the other model to perform
                    similarly to the Model, including - but not limited to - distillation methods entailing the use of
                    intermediate data representations or methods based on the generation of synthetic data by the Model
                    for training the other model.
                  </li>
                  <li>
                    "Complementary Material" means the accompanying source code and scripts used to define, run, load,
                    benchmark or evaluate the Model, and used to prepare data for training or evaluation, if any. This
                    includes any accompanying documentation, tutorials, examples, etc, if any.
                  </li>
                  <li>
                    "Distribution" means any transmission, reproduction, publication or other sharing of the Model or
                    Derivatives of the Model to a third party, including providing the Model as a hosted service made
                    available by electronic or other remote means - e.g. API-based or web access.
                  </li>
                  <li>
                    "Licensor" means the copyright owner or entity authorized by the copyright owner that is granting
                    the License, including the persons or entities that may have rights in the Model and/or distributing
                    the Model.
                  </li>
                  <li>
                    "You" (or "Your") means an individual or Legal Entity exercising permissions granted by this License
                    and/or making use of the Model for whichever purpose and in any field of use, including usage of the
                    Model in an end-use application - e.g. chatbot, translator, image generator.
                  </li>
                  <li>
                    "Third Parties" means individuals or legal entities that are not under common control with Licensor
                    or You.
                  </li>
                  <li>
                    "Contribution" means any work of authorship, including the original version of the Model and any
                    modifications or additions to that Model or Derivatives of the Model thereof, that is intentionally
                    submitted to Licensor for inclusion in the Model by the copyright owner or by an individual or Legal
                    Entity authorized to submit on behalf of the copyright owner. For the purposes of this definition,
                    "submitted" means any form of electronic, verbal, or written communication sent to the Licensor or
                    its representatives, including but not limited to communication on electronic mailing lists, source
                    code control systems, and issue tracking systems that are managed by, or on behalf of, the Licensor
                    for the purpose of discussing and improving the Model, but excluding communication that is
                    conspicuously marked or otherwise designated in writing by the copyright owner as "Not a
                    Contribution."
                  </li>
                  <li>
                    "Contributor" means Licensor and any individual or Legal Entity on behalf of whom a Contribution has
                    been received by Licensor and subsequently incorporated within the Model.
                  </li>
                </ul>
                <h3 className="my-[1.6rem]">Section II: INTELLECTUAL PROPERTY RIGHTS</h3>
                <p className="mb-[1.6rem]">
                  Both copyright and patent grants apply to the Model, Derivatives of the Model and Complementary
                  Material. The Model and Derivatives of the Model are subject to additional terms as described in
                  Section III.
                </p>
                {renderList(
                  'Grant of Copyright License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare, publicly display, publicly perform, \n' +
                    'sublicense, and distribute the Complementary Material, the Model, and Derivatives of the Model.',
                )}
                {renderList(
                  'Grant of Patent License. Subject to the terms and conditions of this License and where and as applicable, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this paragraph) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Model and the Complementary Material, where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Model to which such Contribution(s) was submitted. If You institute patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Model and/or Complementary Material or a Contribution incorporated within the Model and/or Complementary Material constitutes direct or contributory patent infringement, then any patent licenses granted to You under this License for the Model and/or Work shall terminate as of the date such litigation is asserted or filed.',
                )}
                <h3 className="my-[1.6rem]">Section III: CONDITIONS OF USAGE, DISTRIBUTION AND REDISTRIBUTION</h3>
                {renderList(
                  'Distribution and Redistribution. You may host for Third Party remote access purposes (e.g. software-as-a-service), reproduce and distribute copies of the Model or Derivatives of the Model thereof in any medium, with or without modifications, provided that You meet the following conditions:',
                )}
                <ul>
                  <li>
                    Use-based restrictions as referenced in paragraph 5 MUST be included as an enforceable provision by
                    You in any type of legal agreement (e.g. a license) governing the use and/or distribution of the
                    Model or Derivatives of the Model, and You shall give notice to subsequent users You Distribute to,
                    that the Model or Derivatives of the Model are subject to paragraph 5. This provision does not apply
                    to the use of Complementary Material.
                  </li>
                  <li>
                    You must give any Third Party recipients of the Model or Derivatives of the Model a copy of this
                    License;
                  </li>
                  <li>
                    You must cause any modified files to carry prominent notices stating that You changed the files;
                  </li>
                  <li>
                    You must retain all copyright, patent, trademark, and attribution notices excluding those notices
                    that do not pertain to any part of the Model, Derivatives of the Model.
                  </li>
                  <li>
                    You may add Your own copyright statement to Your modifications and may provide additional or
                    different license terms and conditions - respecting paragraph 4.a. - for use, reproduction, or
                    Distribution of Your modifications, or for any such Derivatives of the Model as a whole, provided
                    Your use, reproduction, and Distribution of the Model otherwise complies with the conditions stated
                    in this License.
                  </li>
                </ul>
                {renderList(
                  'Use-based restrictions. The restrictions set forth in Attachment A are considered Use-based restrictions. Therefore You cannot use the Model and the Derivatives of the Model for the specified restricted uses. You may use the Model subject to this License, including only for lawful purposes and in accordance with the License. Use may include creating any content with, finetuning, updating, running, training, evaluating and/or reparametrizing the Model. You shall require all of Your users who use \n' +
                    'the Model or a Derivative of the Model to comply with the terms of this paragraph (paragraph 5).',
                )}
                {renderList(
                  'The Output You Generate. Except as set forth herein, Licensor claims no rights in the Output You generate using the Model. You are accountable for the Output you generate and its subsequent uses. No use of the output can contravene any provision as stated in the License.',
                )}
                <h3 className="my-[1.6rem]">Section IV: OTHER PROVISIONS</h3>
                {renderList(
                  'Updates and Runtime Restrictions. To the maximum extent permitted by law, Licensor reserves the right to restrict (remotely or otherwise) usage of the Model in violation of this License, update the Model through electronic means, or modify the Output of the Model based on updates. You shall undertake reasonable efforts to use the latest version of the Model.',
                )}
                {renderList(
                  'Trademarks and related. Nothing in this License permits You to make use of Licensors’ trademarks, trade names, logos or to otherwise suggest endorsement or misrepresent the relationship between the parties; and any rights not expressly granted herein are reserved by the Licensors.',
                )}
                {renderList(
                  'Disclaimer of Warranty. Unless required by applicable law or agreed to in writing, Licensor provides the Model and the Complementary Material (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Model, Derivatives of the Model, and the Complementary Material and assume any risks associated with Your exercise of permissions under this License.',
                )}
                {renderList(
                  'Limitation of Liability. In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Model and the Complementary Material (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.',
                )}
                {renderList(
                  'Accepting Warranty or Additional Liability. While redistributing the Model, Derivatives of the Model and the Complementary Material thereof, You may choose to offer, and charge a fee for, acceptance of support, warranty, indemnity, or other liability obligations and/or rights consistent with this License. However, in accepting such obligations, You may act only on Your own behalf and on Your sole responsibility, not on behalf of any other Contributor, and only if You agree to indemnify, defend, and hold each Contributor harmless for any liability incurred by, or claims asserted against, such Contributor by reason of your accepting any such warranty or additional liability.',
                )}
                {renderList(
                  'If any provision of this License is held to be invalid, illegal or unenforceable, the remaining provisions shall be unaffected thereby and remain valid as if such provision had not been set forth herein.',
                )}
                <h3 className="my-[1.6rem]">END OF TERMS AND CONDITIONS</h3>
              </ol>
              <br />
              <br />
              <h3>Attachment A</h3>
              <h3 className="my-[2.6rem]">Use Restrictions</h3>
              <p className="mb-[0.6rem]">You agree not to use the Model or Derivatives of the Model:</p>
              <ul>
                <li>
                  In any way that violates any applicable national, federal, state, local or international law or
                  regulation;
                </li>
                <li>For the purpose of exploiting, harming or attempting to exploit or harm minors in any way;</li>
                <li>
                  To generate or disseminate verifiably false information and/or content with the purpose of harming
                  others;
                </li>
                <li>
                  To generate or disseminate personal identifiable information that can be used to harm an individual;
                </li>
                <li>To defame, disparage or otherwise harass others;</li>
                <li>
                  For fully automated decision making that adversely impacts an individual’s legal rights or otherwise
                  creates or modifies a binding, enforceable obligation;
                </li>
                <li>
                  For any use intended to or which has the effect of discriminating against or harming individuals or
                  groups based on online or offline social behavior or known or predicted personal or personality
                  characteristics;
                </li>
                <li>
                  To exploit any of the vulnerabilities of a specific group of persons based on their age, social,
                  physical or mental characteristics, in order to materially distort the behavior of a person pertaining
                  to that group in a manner that causes or is likely to cause that person or another person physical or
                  psychological harm;
                </li>
                <li>
                  For any use intended to or which has the effect of discriminating against individuals or groups based
                  on legally protected characteristics or categories;
                </li>
                <li>To provide medical advice and medical results interpretation;</li>
                <li>
                  To generate or disseminate information for the purpose to be used for administration of justice, law
                  enforcement, immigration or asylum processes, such as predicting an individual will commit fraud/crime
                  commitment (e.g. by text profiling, drawing causal relationships between assertions made in documents,
                  indiscriminate and arbitrarily-targeted use).
                </li>
              </ul>
            </div>
          </>
        )}
        {state === 'attachment-b' && (
          <>
            <div className="flex">
              <div
                className="mr-[1rem] h-[2.1rem] w-[2.1rem] cursor-pointer bg-contain bg-no-repeat"
                style={{ backgroundImage: `url(${renderIcon('back')})` }}
                onClick={handleReset}
              />
              <h2 className="mb-[0.6rem] text-left text-[1.4rem]">
                {bold('Attachment B')} - Golem Image Generator - Terms of Use
              </h2>
            </div>
            <h2 className="my-[2.6rem] text-18">Content Policy</h2>
            <ol className="text-justify">
              {renderList(
                'By using the Golem Image Generator, you confirm that you will not use the Golem Image Generator:',
                [
                  <>
                    In any way that violates any applicable national, federal, state, local or international law or
                    regulation;
                  </>,
                  <>For the purpose of exploiting, harming or attempting to exploit or harm minors in any way;</>,
                  <>
                    To generate or disseminate verifiably false information and/or content with the purpose of harming
                    others;
                  </>,
                  <>
                    To generate or disseminate personal identifiable information that can be used to harm an individual;
                  </>,
                  <>To defame, disparage or otherwise harass others;</>,
                  <>
                    For fully automated decision making that adversely impacts an individual’s legal rights or otherwise
                    creates or modifies a binding, enforceable obligation;
                  </>,
                  <>
                    For any use intended to or which has the effect of discriminating against or harming individuals or
                    groups based on online or offline social behavior or known or predicted personal or personality
                    characteristics;
                  </>,
                  <>
                    To exploit any of the vulnerabilities of a specific group of persons based on their age, social,
                    physical or mental characteristics, in order to materially distort the behavior of a person
                    pertaining to that group in a manner that causes or is likely to cause that person or another person
                    physical or psychological harm;
                  </>,
                  <>
                    For any use intended to or which has the effect of discriminating against individuals or groups
                    based on legally protected characteristics or categories;
                  </>,
                  <>To provide medical advice and medical results interpretation;</>,
                  <>
                    To generate or disseminate information for the purpose to be used for administration of justice, law
                    enforcement, immigration or asylum processes, such as predicting an individual will commit
                    fraud/crime commitment (e.g. by text profiling, drawing causal relationships between assertions made
                    in documents, indiscriminate and arbitrarily-targeted use)
                  </>,
                ],
              )}
              {renderList(
                'The specific types of use listed above are representative, but not exhaustive. If you are uncertain as to whether or not your use of the Golem Image Generator involves a above mentioned prohibited use, or have questions about how these requirements apply to you, please contact us at office@golem.network.',
              )}
              {renderList(
                'When sharing your work, we encourage you to proactively disclose AI/ML involvement in your work.',
              )}
              {renderList(
                'You may remove the Golem’s signature (if any) if you wish, but you may not mislead others about the nature of the work produced by Golem Image Generator. For example, you may not tell people that the work was entirely human generated or that the work is an unaltered photograph of a real event.',
              )}
              {renderList('Respect the rights of others:', [
                <>Do not upload images of people without their consent.</>,
                <>Do not upload images to which you do not hold appropriate usage rights.</>,
                <>Do not create images of public figures.</>,
              ])}
              {renderList(
                'Please report any suspected violations of these rules to our team through our Discord.',
                [],
                true,
              )}
            </ol>
          </>
        )}
      </div>
    </Layout>
  );
}

export default Terms;

function renderList(title: string, items?: ReactNode[], bold?: boolean) {
  return (
    <li>
      <span className={bold ? 'font-bold' : ''}>{title}</span>
      {!!items?.length && (
        <ol>
          {items.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ol>
      )}
    </li>
  );
}

function underline(text: string) {
  return <span className="underline">{text}</span>;
}

function bold(text: string) {
  return <span className="font-bold">{text}</span>;
}

function link(text: string, href?: string) {
  return (
    <a className="text-blue" href={href ?? text} target="_blank" rel="noreferrer">
      {text}
    </a>
  );
}
