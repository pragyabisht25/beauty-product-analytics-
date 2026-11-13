# Case Study: Beauty Product Growth & Recommendation Analytics

**Approach:** Problem Understanding → Data Analysis → Key Findings → Product Opportunity → Proposed Solution → MVP → Success Metrics → A/B Testing

## 1. Business Context

The project is based on a beauty and cosmetics e-commerce platform that sells products across categories such as Skincare, Makeup, Haircare, Fragrance and Personal Care.

The main objective was to understand how customers discover products, interact with them and eventually make a purchase. I wanted to identify where customers were dropping off during their shopping journey and what could be improved to make product discovery easier.

For this analysis, I worked with a synthetic dataset containing 6,000 customers, 330 products, approximately 200,000 user activity events and around 16,000 orders.

## 2. Data Analysis & Key Findings

After analyzing customer activity, product performance and purchase behaviour, I found a few patterns worth investigating.

### 2.1 Product Discovery Funnel

The overall shopping funnel showed that customers were interested in exploring products, but not all of them moved towards a purchase.

- Product Views: 100,277
- Add to Cart: 31,904
- Purchases: 16,252

Around 31.8% of product views resulted in an add-to-cart action, while 50.9% of cart additions resulted in a purchase. Overall, only 16.2% of product views led to a purchase.

This indicated that there was room to improve the journey between product discovery and purchase.

### 2.2 Category and Subcategory Performance

Skincare and Makeup were the most viewed and purchased categories. This suggested that the overall category-level demand was not the main issue.

However, when I looked deeper into individual subcategories, I noticed a difference in purchase conversion.

Subcategories with 20 or more similar products, including Moisturizer, Face Serum, Foundation, Lipstick, Shampoo and Sunscreen, had approximately 11% view-to-purchase conversion.

In comparison, subcategories with fewer and more differentiated products, such as Blush and Body Lotion, had around 20% conversion.

Customers browsing these choice-heavy subcategories also showed higher drop-offs at different stages:

- Around 75% of views did not lead to an add-to-cart action, compared to 63% in low-choice subcategories.
- Cart-to-purchase drop-off was around 56%, compared to 46% in low-choice subcategories.

This made product selection a more interesting area to investigate.

### 2.3 Wishlist Activity and Product Ratings

I also looked at products that received attention but did not convert well.

- 43 products had high wishlist activity but low wishlist-to-purchase conversion.
- 60 products had ratings of 4.3 or above but still converted below the platform median.

This suggested that customers were interested in these products, but their interest was not always turning into purchases.

It also showed that good ratings alone were not enough to explain purchase behaviour.

### 2.4 Impact of Discounts

I checked the relationship between discounts and purchase behaviour.

The correlation between discount percentage and view-to-cart conversion was 0.54, while the correlation with view-to-purchase conversion was 0.64.

Discounts showed a positive association with conversion, but this does not necessarily mean that discounts directly caused more purchases. Other factors, such as customer preferences and existing product demand, could also influence these results.

### 2.5 Impact of Product Ratings

I expected highly rated products to have noticeably better conversion rates. However, the analysis showed that view-to-purchase conversion remained around 15–16% across different rating bands.

This was another indication that product ratings alone were not solving the purchase decision problem.

*Supporting analysis: `charts/02_choice_heavy_conversion.png`, `charts/03_discount_vs_conversion.png`, `charts/04_overall_funnel.png`. Detailed results are available in `docs/analysis_output.txt` and `data/derived/`.*

## 3. Key Insight

The most important finding was the difference between customer interest and actual purchases in subcategories with many similar products.

Customers were viewing products and adding them to their wishlists, but a much smaller percentage were completing their purchases.

After looking at ratings, discounts and funnel performance, I found that the problem was not simply a lack of product interest or product quality.

One possible reason was the difficulty of choosing between too many similar options.

This led me to explore how a better product comparison experience could help customers make decisions.

## 4. Product Opportunity

The opportunity was to make product selection easier, especially in subcategories where customers had many similar options.

For example, a customer might shortlist four different moisturizers but still struggle to understand which one is more suitable based on price, ratings, benefits or skin type.

Instead of showing more products or offering additional discounts, the platform could help customers compare the products they were already interested in.

## 5. Proposed Solution: Compare Products Feature

Based on the findings, I proposed a feature called **Compare Products**.

The feature would allow customers to select up to three products from the same subcategory and view their details side by side.

Customers would be able to compare:

- Product price and discount
- Customer ratings and reviews
- Skin or hair suitability
- Key product benefits
- Other important product details

A direct Add to Cart option would also be available from the comparison screen.

The aim is to help customers understand the differences between similar products without having to open and check each product separately.

## 6. MVP Scope

For the first version, I kept the feature limited to the most important functionality.

**Included in MVP:**

- Add to Compare option on product listing cards and product detail pages.
- Selection of a maximum of three products from the same subcategory.
- A comparison tray to manage selected products.
- A comparison screen showing the main product attributes.
- Add to Cart option for each product.
- Comparison suggestions in the six identified choice-heavy subcategories.

**Not included in the first version:**

- Comparison across different subcategories.
- AI-based product recommendations.
- Ingredient-matching functionality.
- Comparison of detailed customer review content.

Keeping the first version focused would make it easier to test whether the feature actually helps customers.

## 7. Success Metrics

I identified the following metrics to evaluate the feature after launch.

**Primary Metric**

- View-to-purchase conversion rate in choice-heavy subcategories.

**Secondary Metrics**

- Percentage of users using the Compare feature.
- Conversion rate after using the comparison screen.
- View-to-cart conversion rate.
- Repeat usage of the feature.

**Guardrail Metrics**

- Overall platform conversion rate.
- Time spent on product detail pages.
- Product listing page load time.

These metrics would help measure both feature usage and its actual impact on purchases.

## 8. A/B Testing Plan

Before making the feature available to everyone, I would test it through an A/B experiment.

**Hypothesis:**

Providing a simple way to compare similar products will help customers make purchase decisions more easily and improve view-to-purchase conversion in choice-heavy subcategories.

**Experiment Setup**

- **Target Users:** Customers browsing Moisturizer, Face Serum, Foundation, Lipstick, Shampoo and Sunscreen.
- **Control Group:** Users continue with the existing shopping experience.
- **Variant Group:** Users get access to the Compare Products feature.
- **Randomization:** Users are assigned to groups at the user level to avoid mixing experiences.

**Metrics to Track**

The primary metric would be view-to-purchase conversion in the selected subcategories.

Other metrics would include feature adoption, comparison-to-purchase conversion, view-to-cart conversion and cart-to-purchase conversion.

Overall conversion, page loading time and product detail page engagement would be monitored as guardrail metrics.

**Experiment Duration and Sample Size**

The experiment should run long enough to collect sufficient data for a reliable result.

Based on the dataset, the identified subcategories have approximately 7,100 views per week per subcategory. Before launching, I would calculate the required sample size using the existing 11% conversion baseline and a minimum detectable improvement of 2 percentage points.

**Success Criteria**

The feature would be considered successful if it produces a statistically significant improvement in the primary metric without a meaningful negative impact on the guardrail metrics.

If customers use the feature but purchase conversion does not improve, I would investigate other possible reasons, such as pricing, product trust or missing product information.

## 9. Limitations

There are a few limitations to consider while interpreting these findings:

- The analysis uses synthetic data, not actual customer data from a live e-commerce platform.
- The difference in conversion between choice-heavy and low-choice subcategories shows an association, not proof that having more products causes lower conversion.
- Discount and rating relationships are also observational. Other factors, such as brand trust, delivery time and product images, were not included in the analysis.
- The choice-heavy classification is based on the number of similar SKUs in each subcategory. In a real business, this definition should also be validated through customer feedback, surveys and user behaviour research.

A real A/B test would be required to understand whether the proposed feature actually improves conversion.

## 10. Final Recommendation

Based on the analysis, I would recommend testing the Compare Products feature in the six identified choice-heavy subcategories first.

The initial rollout should be limited to an MVP, followed by an A/B test to measure its impact on customer behaviour and purchase conversion.

If the results are positive, the feature could be extended to other categories, with further improvements such as personalized recommendations in future versions.

The main goal is to make product selection easier and help customers move from browsing and shortlisting to making a purchase.
