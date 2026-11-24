                                        "required": [
                                            "title",
                                            "description",
                                            "notes"
                                        ],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            max_output_tokens=600,
                            store=False
                        )

                        correction = json.loads(
                            response.output_text
                        )

                        results.append({
                            "row_number": index + 1,
                            "sku": product["sku"],
                            "original_title": product["title"],
                            "suggested_title": correction["title"],
                            "original_description": product["description"],
                            "suggested_description": correction["description"],
                            "original_price": product["price"],
                            "notes": correction["notes"],
                            "status": "Review required"
                        })

                    except Exception:

                        results.append({
                            "row_number": index + 1,
                            "sku": product["sku"],
                            "original_title": product["title"],
                            "suggested_title": "",
                            "original_description": product["description"],
                            "suggested_description": "",
                            "original_price": product["price"],
                            "notes": "AI request failed.",
                            "status": "Error"
                        })

                        break

                    progress.progress(
                        (number + 1) / len(targets)
                    )

                st.session_state["ai_results"] = results
                st.session_state["ai_file_id"] = file_id
                st.session_state["ai_language"] = language

            except Exception:

                st.error(
                    "AI connection failed. Check API "
                    "credentials, billing and model access."
                )

        if (
            st.session_state.get("ai_results")
            and st.session_state.get("ai_file_id") == file_id
            and st.session_state.get("ai_language") == language
        ):

            result_df = pd.DataFrame(
                st.session_state["ai_results"]
            )

            completed = int(
                result_df["status"].eq(
                    "Review required"
                ).sum()
            )

            st.subheader("AI Correction Results")

            st.write(
                f"{completed} products processed successfully."
            )

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )

            if completed > 0:

                st.download_button(
                    "Download AI Correction Suggestions",
                    safe_csv(result_df),
                    "catalogfix_ai_corrections.csv",
                    "text/csv"
                )

            if completed < len(targets):
                st.warning(
                    "Processing may be incomplete. Check "
                    "the results and API billing if needed."
                )

st.divider()

st.header("Make Your Product Catalog Store-Ready")

st.write(
    "CatalogFix AI helps online stores identify "
    "product data issues before importing supplier catalogs."
)

st.divider()
st.header("Plans & Pricing")
PAYMENT_LINKS = {
    "Pilot": "https://buy.stripe.com/7sYbIT42DfW28wy6Zlew800",
    "Pro": "https://buy.stripe.com/14A5kvdDd4dk3ce0AXew801",
    "Business": "https://buy.stripe.com/00waEP6aLaBI5km1F1ew802",
    "Enterprise": "https://buy.stripe.com/eVq6oz42DeRYcMOabxew803",
}
# Enable only after the corresponding service is ready for delivery.
PILOT_READY = False
SUBSCRIPTIONS_READY = False

st.write("Choose the right plan for your business.")

p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    st.subheader("Free Demo")
    st.title("€0")
    st.caption("Free forever")
    st.markdown("""
    - Up to 100 products
    - Automatic error detection
    - Quality dashboard
    - CSV audit report
    """)

with p2:
    st.subheader("Pilot Service")
    st.title("€49")
    st.caption("One-time payment")
    st.markdown("""
    - Up to 100 products
    - Detailed data review
    - AI-assisted text suggestions
    - Reviewed correction report
    """)
    if PILOT_READY:
        st.link_button("Buy Pilot — €49", PAYMENT_LINKS["Pilot"])
        st.caption("Manual delivery. Contact us after payment for next steps.")
    else:
        st.link_button("Request Pilot", "mailto:catalogfixai1@gmail.com?subject=Pilot%20Service")

with p3:
    st.subheader("Pro")
    st.title("€99")
    st.caption("Per month - planned")
    st.markdown("""
    - Up to 2,000 products/month
    - AI text optimization
    - Automatic data checks
    - Corrected CSV export
    """)
    if SUBSCRIPTIONS_READY:
        st.link_button("Subscribe to Pro", PAYMENT_LINKS["Pro"])
    else:
        st.info("Coming soon")
        st.link_button("Join waitlist", "mailto:catalogfixai1@gmail.com?subject=Pro%20Waitlist")

with p4:
    st.subheader("Business")
    st.title("€299")
    st.caption("Per month - planned")
    st.markdown("""
   - Up to 50,000 products/month
    - Bulk AI optimization
    - Advanced quality reports
    - Priority processing
    """)
    if SUBSCRIPTIONS_READY:
        st.link_button("Subscribe to Business", PAYMENT_LINKS["Business"])
    else:
        st.info("Coming soon")
        st.link_button("Join waitlist", "mailto:catalogfixai1@gmail.com?subject=Business%20Waitlist")

with p5:
    st.subheader("Enterprise")
    st.title("€599")
    st.caption("Custom pricing available")
    st.markdown("""
