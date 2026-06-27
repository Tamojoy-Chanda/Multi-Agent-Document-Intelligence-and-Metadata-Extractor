import os
from typing import TypedDict, Annotated, Dict, Any, Type
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# Ensure API key is available
# os.environ["OPENAI_API_KEY"] = "your-key"

class AgentState(TypedDict):
    text: str
    category: str
    metadata: Dict[str, Any]

# Pydantic models for structured output
class DocumentCategory(BaseModel):
    category: str = Field(description="The category of the document, e.g., Invoice, Contract, Technical Spec, or Other")

class InvoiceMetadata(BaseModel):
    date: str = Field(description="Date of the invoice")
    total_amount: str = Field(description="Total amount on the invoice")
    vendor: str = Field(description="Vendor or company name")

class ContractMetadata(BaseModel):
    parties: str = Field(description="Parties involved in the contract")
    effective_date: str = Field(description="Effective date of the contract")
    key_terms: str = Field(description="Brief summary of key terms")

def classify_node(state: AgentState):
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a document classifier. Classify the following text into one of these categories: Invoice, Contract, Technical Spec, Other."),
        ("human", "{text}")
    ])
    chain = prompt | llm.with_structured_output(DocumentCategory)
    result = chain.invoke({"text": state["text"][:3000]}) # Use first 3000 chars for classification
    return {"category": result.category}

def extract_node(state: AgentState):
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    category = state["category"]
    
    if "Invoice" in category:
        schema = InvoiceMetadata
        sys_msg = "You are a metadata extractor for invoices. Extract date, total_amount, and vendor."
    elif "Contract" in category:
        schema = ContractMetadata
        sys_msg = "You are a metadata extractor for contracts. Extract parties, effective_date, and key_terms."
    else:
        # Generic extraction
        class GenericMetadata(BaseModel):
            summary: str = Field(description="A brief summary of the document")
            author_or_entity: str = Field(description="The author or primary entity mentioned")
        schema = GenericMetadata
        sys_msg = "You are a metadata extractor. Extract a summary and author/entity."
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        ("human", "{text}")
    ])
    chain = prompt | llm.with_structured_output(schema)
    result = chain.invoke({"text": state["text"][:5000]})
    return {"metadata": result.dict()}

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("classifier", classify_node)
    workflow.add_node("extractor", extract_node)
    
    workflow.set_entry_point("classifier")
    workflow.add_edge("classifier", "extractor")
    workflow.add_edge("extractor", END)
    
    return workflow.compile()

graph = build_graph()

def process_document_text(text: str) -> dict:
    initial_state = {"text": text, "category": "", "metadata": {}}
    result = graph.invoke(initial_state)
    return {
        "category": result["category"],
        "metadata": result["metadata"]
    }
