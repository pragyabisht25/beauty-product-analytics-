# Product Requirements Document (PRD)
## Compare Products – Beauty Product Comparison Feature

**Project:** Beauty Product Growth & Recommendation Analytics  
**Platform:** Beauty & Cosmetics E-commerce  
**Document Status:** Draft  
**Version:** 1.0  
**Related Documents:** `docs/case_study.md`, `data/derived/subcategory_funnel.csv`

---

## 1. Problem Statement

During the analysis, I found that customers browsing subcategories with a large number of similar products were less likely to make a purchase compared to customers browsing subcategories with fewer options.

The analysis showed the following difference:

- Choice-heavy subcategories: 11% view-to-purchase conversion.
- Low-choice subcategories: 20% view-to-purchase conversion.
- View-to-cart drop-off in choice-heavy subcategories: 75%.
- View-to-cart drop-off in low-choice subcategories: 63%.

Subcategories such as Moisturizer, Face Serum, Foundation, Lipstick and Shampoo showed this pattern.

At the same time, wishlist activity in these subcategories was relatively high. This suggested that customers were interested in the products but were not always moving forward with a purchase.

One possible reason is that customers have difficulty choosing between similar products. They may visit multiple product pages, compare details manually and switch between tabs to decide which product suits them better.

Currently, there is no simple way to compare these products side by side.

This creates an opportunity to improve the product selection experience and make purchase decisions easier.

## 2. Target Users

The feature is mainly intended for the following customer groups:

**Primary Users**

- Customers exploring subcategories with many similar products.
- Customers who shortlist multiple products before making a purchase.
- New shoppers who are not familiar with different beauty brands and product options.
- Customers who compare products based on price, ratings, reviews and product benefits.

**Secondary Users**

- Returning customers who want to explore better-priced or better-rated alternatives before purchasing again.

## 3. User Story

"As a beauty shopper, I want to compare multiple similar products in one place based on their price, ratings, reviews and important features, so that I can understand the differences and choose a product without repeatedly opening different product pages."

## 4. Product Goals

The main goals of this feature are:

- Make it easier for customers to compare similar products.
- Reduce the number of customers leaving product pages without adding anything to their cart.
- Improve view-to-purchase conversion in choice-heavy subcategories.
- Help customers understand product differences without manually checking multiple pages.
- Provide a smoother shopping experience for customers who are still deciding between shortlisted products.

## 5. Scope and Non-Goals

The first version will focus on basic product comparison. Some advanced functionalities will be considered for future versions.

**Not included in the MVP:**

- Comparing products from different subcategories, such as a serum and a moisturizer.
- AI-based product recommendations or personalized suggestions.
- Comparing more than three products at once.
- Automatic ingredient matching or allergen detection.
- Detailed comparison of customer review content.

The focus is to first understand whether a simple comparison feature can improve purchase decisions.

## 6. MVP Feature Requirements

The first version of the feature will include the following functionalities:

### 6.1 Add to Compare

- An Add to Compare option will be available on product listing cards and product detail pages.
- Customers can select a maximum of three products.
- Products must belong to the same subcategory.
- Users should be able to remove a selected product and replace it with another.

### 6.2 Compare Tray

- A small comparison tray will appear when customers select products.
- It will display the selected products.
- A Compare Now button will become available after selecting at least two products.
- Customers can remove products directly from the tray.

### 6.3 Product Comparison Screen

The comparison screen will display selected products side by side.

The following details will be included:

| Product Information | Details |
|---|---|
| Basic Details | Product image, name and brand |
| Pricing | Original price, discount and final price |
| Ratings | Average rating and review count |
| Product Attributes | Skin/hair suitability and key benefits |
| Product Size | Volume or quantity |
| Action | Add to Cart button |

Customers should be able to add a product to their cart directly from this screen.

### 6.4 Feature Entry Points

The feature will be accessible from:

- Product listing and search pages through the Add to Compare option.
- Product detail pages through a Compare with Similar Products option.
- The comparison tray, which will remain accessible while browsing.

For the first version, the feature will focus on the identified choice-heavy subcategories.

## 7. User Flow

The expected customer journey is:

```text
Search / Category Browsing
          |
          v
    Product Listing
          |
          v
   Select 2-3 Products
          |
          v
      Compare Tray
          |
          v
  Comparison Screen
          |
          v
   Compare Product Details
          |
          v
      Select Product
          |
          v
       Add to Cart
          |
          v
        Purchase
```

Customers can also reach the comparison experience from a product detail page using the Compare with Similar Products option.

## 8. Success Metrics

The feature will be evaluated based on customer usage and its impact on purchase conversion.

### 8.1 Primary Metric

**View-to-Purchase Conversion Rate**

The main objective is to improve purchase conversion in choice-heavy subcategories.

The initial target is to close approximately 30–40% of the existing 9-percentage-point conversion gap between choice-heavy and low-choice subcategories within one quarter of full rollout.

### 8.2 Secondary Metrics

- **Feature Adoption Rate:** Percentage of sessions in which customers use the Add to Compare option.
- **Comparison-to-Purchase Conversion:** Percentage of comparison-screen sessions that result in an add-to-cart action during the same session.
- **View-to-Cart Rate:** Whether more customers add products to their carts after using the feature.
- **Repeat Usage:** Percentage of customers who use the comparison feature more than once.

### 8.3 Guardrail Metrics

These metrics will help ensure that the new feature does not negatively affect the existing shopping experience.

- Overall site conversion rate.
- Product detail page engagement time.
- Listing page loading time and Core Web Vitals.

## 9. Assumptions and Risks

### Assumptions

- Customers in choice-heavy subcategories may be facing difficulty while comparing similar products.
- Product price, ratings, reviews and benefits are important factors during product selection.
- Showing these details together may help customers make decisions more easily.

These assumptions are based on the available analysis and need to be validated through an experiment.

### Potential Risks and Mitigation

**Risk 1: Customers use the feature but still do not purchase.**

The main issue may be price, product quality or lack of trust rather than comparison difficulty.

*Mitigation:* Track comparison usage and purchase conversion separately to understand where customers are dropping off.

**Risk 2: Customers do not notice the feature.**

If the option is difficult to find, customers may continue using the existing shopping experience.

*Mitigation:* Place Add to Compare directly on product listing cards and product detail pages.

**Risk 3: The feature affects page performance.**

An additional comparison tray or interface could increase page loading time.

*Mitigation:* Keep the comparison interface lightweight and monitor page performance after implementation.

**Risk 4: Too many product details make comparison difficult.**

Showing too much information may make the screen confusing, especially on mobile devices.

*Mitigation:* Keep the MVP limited to the most useful product attributes.

## 10. Validation Plan

Before releasing the feature across the platform, I would validate it through an A/B test.

- **Control Group:** Customers continue using the existing shopping experience.
- **Variant Group:** Customers get access to the Compare Products feature.
- **Target Audience:** Customers browsing the six identified choice-heavy subcategories.
- **Primary Evaluation:** Compare view-to-purchase conversion between both groups.
- **Additional Evaluation:** Track feature adoption, add-to-cart behaviour and guardrail metrics.

The feature should be expanded only if the experiment shows a meaningful improvement in purchase conversion without negatively affecting the overall shopping experience.

## 11. Future Improvements

If the initial version performs well, the feature can be improved further.

Possible future additions include:

- Personalized product suggestions based on customer preferences.
- Better ingredient and skin-type comparisons.
- Comparison across additional product categories.
- More detailed product review comparisons.
- Recommendations based on previously viewed or shortlisted products.

These improvements can be considered after evaluating the results of the first version.

## 12. Final Recommendation

Based on the analysis, I recommend starting with a simple Compare Products feature for the six identified choice-heavy subcategories.

The first version should focus on helping customers compare products using the information already available on the platform.

Instead of introducing multiple advanced features at once, the MVP should first be tested to understand whether easier product comparison actually improves customer decisions and purchase conversion.

The results of the experiment will help decide whether the feature should be expanded or improved further.
